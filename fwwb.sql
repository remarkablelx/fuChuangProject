/*
 Navicat Premium Dump SQL

 Source Server         : FC
 Source Server Type    : MySQL
 Source Server Version : 80041 (8.0.41)
 Source Host           : localhost:3306
 Source Schema         : flask

 Target Server Type    : MySQL
 Target Server Version : 80041 (8.0.41)
 File Encoding         : 65001

 Date: 26/03/2025 14:52:41
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for user_videos
-- ----------------------------
DROP TABLE IF EXISTS `user_videos`;
CREATE TABLE `user_videos`  (
  `video_id` varchar(512) NOT NULL COMMENT '主键ID',
  `user_id` int NOT NULL COMMENT '用户ID，外键',
  `video_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '视频存储路径',
  PRIMARY KEY (`video_id` DESC) USING BTREE,
  INDEX `fk_user_videos_user`(`user_id` ASC) USING BTREE,
  CONSTRAINT `fk_user_videos_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_videos
-- ----------------------------

-- ----------------------------
-- Table structure for user_videos_process
-- ----------------------------
DROP TABLE IF EXISTS `user_videos_process`;
CREATE TABLE `user_videos_process`  (
  `video_id` varchar(512) NOT NULL COMMENT '主键ID',
  `user_id` int NOT NULL COMMENT '用户ID，外键',
  `video_path_process` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '视频存储路径',
  PRIMARY KEY (`video_id` DESC) USING BTREE,
  INDEX `fk_user_videos_user_process`(`user_id` ASC) USING BTREE,
  CONSTRAINT `fk_user_videos_user_process` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user_videos_process
-- ----------------------------

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password_hash` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`user_id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE,
  UNIQUE INDEX `phone`(`phone` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, '张三', '19100000003', 'pbkdf2:sha256:1000000$G9avP4gLoQTjxmNA$4a865708bd41c0655b87118f0066dab7ff2d5d56f064a09e3b259c37040abd27');
INSERT INTO `users` VALUES (2, '李四', '19100000004', 'pbkdf2:sha256:1000000$5OQydItRmXJ7Iej8$58ead136848f7c0df3b91bbbf1b71101a0d1656d50e7136b8c4490b1938d613c');
INSERT INTO `users` VALUES (6, '王五', '19100000005', 'pbkdf2:sha256:1000000$Ehtwp4i4exV2bysj$546fd73b68075c1fbd6d1b797087c9ed07cddb3e00157302567ded6315c01600');

-- ----------------------------
-- Table structure for video_frames
-- ----------------------------
DROP TABLE IF EXISTS `video_frames`;
CREATE TABLE `video_frames`  (
  `frame_id` varchar(512) NOT NULL COMMENT '主键ID',
  `video_id` varchar(512) NOT NULL COMMENT '视频ID\r\n视频ID，外键',
  `frame_index` int NOT NULL COMMENT '帧序号',
  `frame_path` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '帧图片路径',
  PRIMARY KEY (`frame_id`) USING BTREE,
  INDEX `fk_frames_video`(`video_id` ASC) USING BTREE,
  CONSTRAINT `fk_frames_video` FOREIGN KEY (`video_id`) REFERENCES `user_videos` (`video_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of video_frames
-- ----------------------------

-- ----------------------------
-- Table structure for video_frames_process
-- ----------------------------
DROP TABLE IF EXISTS `video_frames_process`;
CREATE TABLE `video_frames_process`  (
  `frame_id` varchar(512) NOT NULL COMMENT '主键ID',
  `video_id` varchar(512) NOT NULL COMMENT '\r\n视频ID，外键',
  `frame_index` int NOT NULL COMMENT '帧序号',
  `frame_path_process` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '帧图片路径',
  PRIMARY KEY (`frame_id`) USING BTREE,
  INDEX `fk_frames_video_process`(`video_id` ASC) USING BTREE,
  CONSTRAINT `fk_frames_video_process` FOREIGN KEY (`video_id`) REFERENCES `user_videos` (`video_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of video_frames_process
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
