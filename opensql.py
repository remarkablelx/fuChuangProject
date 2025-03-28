import sqlite3
import mysql.connector
from mysql.connector import Error

# ================= 配置部分 =================
sqlite_db = "id_cache.db"
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'lx20040622',
    'database': 'flask'
}


# ============================================

def convert_sqlite_type(sqlite_type):
    """转换 SQLite 数据类型到 MySQL"""
    type_mapping = {
        'INTEGER': 'INT',
        'TEXT': 'LONGTEXT',  # Changed from VARCHAR(255) to LONGTEXT
        'BLOB': 'LONGBLOB',
        'REAL': 'FLOAT',
        'NUMERIC': 'DECIMAL(10,2)'
    }
    return type_mapping.get(sqlite_type.upper(), 'LONGTEXT')  # Default to LONGTEXT


def get_table_schema(conn_sqlite, table_name):
    """获取并转换表结构"""
    cursor = conn_sqlite.execute(f"PRAGMA table_info({table_name})")

    columns = []
    primary_keys = []

    for row in cursor:
        col_name = row[1]
        col_type = convert_sqlite_type(row[2])
        is_pk = row[5] > 0

        # 处理自增字段
        if is_pk and 'AUTOINCREMENT' in str(row):
            col_type += ' AUTO_INCREMENT'

        columns.append(f"`{col_name}` {col_type}")
        if is_pk:
            primary_keys.append(f"`{col_name}`")

    # 构建建表语句
    create_table = f"CREATE TABLE IF NOT EXISTS `{table_name}` (\n"
    create_table += ",\n".join(columns)

    # 添加主键
    if primary_keys:
        create_table += f",\nPRIMARY KEY ({', '.join(primary_keys)})"

    # 获取外键约束
    cursor = conn_sqlite.execute(f"PRAGMA foreign_key_list({table_name})")
    fk_constraints = []

    for fk in cursor:
        fk_constraint = (
            f"FOREIGN KEY (`{fk[3]}`) "
            f"REFERENCES `{fk[2]}` (`{fk[4]}`) "
            f"ON DELETE {fk[5] or 'NO ACTION'} "
            f"ON UPDATE {fk[6] or 'NO ACTION'}"
        )
        fk_constraints.append(fk_constraint)

    if fk_constraints:
        create_table += ",\n" + ",\n".join(fk_constraints)

    create_table += "\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
    return create_table


def migrate_table(conn_sqlite, conn_mysql, table_name):
    """迁移单个表"""
    # 获取建表语句
    create_sql = get_table_schema(conn_sqlite, table_name)

    # 在 MySQL 中创建表
    mysql_cursor = conn_mysql.cursor()
    try:
        mysql_cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`")
        mysql_cursor.execute(create_sql)
    except Error as e:
        print(f"创建表 {table_name} 失败: {e}")
        return

    # 迁移数据（保持事务）
    try:
        # 禁用外键检查
        mysql_cursor.execute("SET FOREIGN_KEY_CHECKS=0")

        # 获取 SQLite 数据
        sqlite_cursor = conn_sqlite.execute(f"SELECT * FROM `{table_name}`")
        columns = [desc[0] for desc in sqlite_cursor.description]
        placeholders = ', '.join(['%s'] * len(columns))

        # 批量插入
        batch_size = 1000
        insert_sql = f"INSERT INTO `{table_name}` ({', '.join(columns)}) VALUES ({placeholders})"

        while True:
            rows = sqlite_cursor.fetchmany(batch_size)
            if not rows:
                break
            # 转换 BLOB 类型
            converted_rows = []
            for row in rows:
                converted_row = list(row)
                for i, value in enumerate(converted_row):
                    if isinstance(value, bytes):
                        converted_row[i] = value.hex()  # 处理二进制数据
                converted_rows.append(converted_row)
            mysql_cursor.executemany(insert_sql, converted_rows)
            conn_mysql.commit()

        print(f"表 {table_name} 迁移完成，共迁移 {len(converted_rows)} 条记录")

    except Error as e:
        print(f"迁移数据到 {table_name} 失败: {e}")
        conn_mysql.rollback()
    finally:
        # 重新启用外键检查
        mysql_cursor.execute("SET FOREIGN_KEY_CHECKS=1")
        mysql_cursor.close()


def get_all_tables(conn_sqlite):
    """获取所有表名"""
    cursor = conn_sqlite.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [row[0] for row in cursor.fetchall()]


def get_dependent_tables(conn_sqlite):
    """获取表依赖关系"""
    tables = get_all_tables(conn_sqlite)
    dependencies = {}

    for table in tables:
        dependencies[table] = []
        cursor = conn_sqlite.execute(f"PRAGMA foreign_key_list({table})")
        for fk in cursor.fetchall():
            dependencies[table].append(fk[2])  # fk[2] 是被引用的表名

    return dependencies


def get_table_order(dependencies):
    """根据依赖关系获取表的创建顺序"""
    result = []
    visited = set()

    def visit(table):
        if table in visited:
            return
        visited.add(table)
        for dep in dependencies.get(table, []):
            visit(dep)
        result.append(table)

    for table in dependencies:
        visit(table)

    return result


def main():
    try:
        # 连接到 SQLite
        conn_sqlite = sqlite3.connect(sqlite_db)

        # 连接到 MySQL
        conn_mysql = mysql.connector.connect(**mysql_config)

        # 获取所有表及其依赖关系
        dependencies = get_dependent_tables(conn_sqlite)

        # 按依赖顺序排序表
        tables_order = get_table_order(dependencies)

        print(f"将按以下顺序迁移表: {tables_order}")

        for table in tables_order:
            migrate_table(conn_sqlite, conn_mysql, table)

    except Error as e:
        print(f"数据库连接失败: {e}")
    finally:
        if conn_sqlite:
            conn_sqlite.close()
        if conn_mysql and conn_mysql.is_connected():
            conn_mysql.close()


if __name__ == "__main__":
    main()