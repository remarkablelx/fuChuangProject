import {
    c as r, o as d, a as s, w as a, C as c, F as m, r as v,
    t as b, D as M, x as h, E as g, h as y, n as f, v as x, G as k
} from "./index-DBcA3JiZ.js";
import { _ as E } from "./Logo-g9zeObaF.js";

const R = {
    data() {
        return {
            messages: [],
            inputMessage: "",
            report: "",
            selectedApi: "qianfan",
            selectedModel: "ernie-x1",
            selectedMode: "custom",
            selectedExpert: "Cybersecurity-RAG",
            graphRagEnabled: !0,
            apiModels: {
                openai: [
                    { value: "gpt-4o", text: "gpt-4o" },
                    { value: "gpt-3.5-turbo", text: "gpt-3.5-turbo" }
                ],
                qianfan: [
                    { value: "ernie-x1", text: "ERNIE X1" },
                    { value: "ernie-4.5", text: "ERNIE 4.5" },
                    { value: "deepseek-r1", text: "DeepSeek R1" },
                    { value: "deepseek-v3", text: "DeepSeek V3" }
                ]
            },
            modes: [
                { value: "custom", label: "自定义" },
                { value: "expert", label: "专家" }
            ],
            isGenerating: false,
        };
    },
    watch: {
        selectedApi(newApi) {
            const models = this.apiModels[newApi];
            if (models && models.length > 0) {
                this.selectedModel = models[0].value;
            } else {
                this.selectedModel = '';
            }
        }
    },
    methods: {
        async sendMessage() {
            const content = this.inputMessage.trim();
            if (!content) return;
            console.log("Sending message:", content);
            this.messages.push({ role: "user", content });
            this.inputMessage = "";
            const prompt = content;
            const mode = this.selectedMode;
            const graphrag = this.graphRagEnabled;
            const chatHistory = this.messages.slice(0, -5).map(({ role, content }) => ({ role, content }));

            try {
                const response = await fetch("/api/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        prompt,
                        chat_history: chatHistory,
                        mode,
                        graphrag,
                        report: this.report,
                        selected_api: this.selectedApi,
                        selected_model: this.selectedModel
                    })
                });
                const data = await response.json()
                let result = data.content;
                for (const chunk of this.mockStream(data.content)) {
                    result += chunk;
                    this.updateAssistantMessage(result);
                }
            } catch (error) {
                console.error("Error:", error);
                this.addMessage("assistant", "抱歉，请求处理失败");
            }
        },
        updateAssistantMessage(o) {
            const e = this.messages[this.messages.length - 1];
            (e == null ? void 0 : e.role) === "assistant"
                ? (e.content = o)
                : this.messages.push({ role: "assistant", content: o });
            this.$nextTick(() => {
                this.$refs.chatHistory.scrollTop = this.$refs.chatHistory.scrollHeight;
            });
        },
        addMessage(o, e) {
            this.messages.push({ role: o, content: e });
            this.$nextTick(() => {
                this.$refs.chatHistory.scrollTop = this.$refs.chatHistory.scrollHeight;
            });
        },
        async handleFileUpload(o) {
            const files = Array.from(o.target.files);
            const formData = new FormData();

            files.forEach(file => formData.append("files", file));

            console.log("Uploading files:", files);

            try {
                const response = await fetch("/api/upload_eval", {
                    method: "POST",
                    body: formData
                });

                const result = await response.json();
                if (response.ok && result.status === "success") {  // 判断 status 字段
                    console.log("文件处理和嵌入生成成功：", result);
                    alert("文件上传成功！知识图谱节点数：" + result.total_nodes + ", 边数：" + result.total_edges);
                } else {
                    console.error("文件上传失败：", result.error || "未知错误");
                    // alert("文件上传失败：" + result.error);
                }
            } catch (error) {
                console.error("上传异常：", error);
                // alert("上传异常：" + error.message);
            }
        },
        clearHistory() {
            this.messages = [];
        },
        toggleModeOptions() { },

        mockStream(text) {
            const lines = text.split('\n');
            return lines;
        },
        async load_embedding() {
            console.log("加载专家嵌入...");
            try {
                this.loading = true;
                const response = await fetch("/api/load_dataset_embedding", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    }
                });
                const result = await response.json();
                if (response.ok && result.status === "success") {
                    console.log("Embedding 加载成功：", result);
                    alert("知识库加载成功！");
                } else {
                    console.error("加载失败：", result.error || "未知错误");
                }
            } catch (error) {
                console.error("请求异常：", error);
            } finally {
                this.loading = false;
            }
        },
        async loadReport() {
            console.log("加载报告...");
            try {
                document.getElementById("download-btn").style.display = "none";
                document.getElementById("generate-btn").style.display = "none";
                document.getElementById("generating-btn").style.display = "inline-block";
                this.loading = true;

                const token = localStorage.getItem("token");  
                // const userId = localStorage.getItem("user_id");

                const response = await fetch("/api/load_report", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}` 
                    },
                    body: JSON.stringify({})  
                });

                const result = await response.json();

                if (result.report) {
                    this.report = result.report;
                    document.getElementById("generate-btn").style.display = "inline-block";
                    document.getElementById("generating-btn").style.display = "none";
                    document.getElementById("download-btn").style.display = "inline-block";
                } else {
                    console.error("未能获取报告内容");
                }
            } catch (error) {
                console.error("请求异常：", error);
            } finally {
                this.loading = false;
            }
        },
        downloadReport() {
            const blob = new Blob([this.report], { type: 'text/plain;charset=utf-8' });
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = '运动动作分析报告.md';
            link.click();
        }
    }
};


const A = { class: "chat-container" };
const U = { class: "sidebar" };
const C = { class: "bar-section model-section" };
const V = { class: "select-group" };
const w = ["value"];
const H = { class: "bar-section mode-section" };
const G = { class: "select-group" };
const D = ["value"];
const F = { class: "bar-section" };
const S = { class: "select-group" };
const T = { class: "chat-wrapper" };
const O = { class: "chat-history", ref: "chatHistory" };
const B = { class: "input-area" };

function I(o, e, i, p, l, n) {
    return d(), r("div", A, [
        s("aside", U, [
            s("div", C, [
                e[15] || (e[15] = s("h4", { class: "section-title" }, "模型切换", -1)),
                s("div", V, [
                    a(s("select", {
                        "onUpdate:modelValue": e[0] || (e[0] = t => l.selectedApi = t),
                        class: "form-select"
                    }, e[14] || (
                        e[14] = [
                            s("option", { value: "qianfan" }, "百度千帆", -1),
                            s("option", { value: "openai" }, "OpenAI", -1)
                        ]
                    ), 512), [[c, l.selectedApi]]),
                    a(s("select", {
                        "onUpdate:modelValue": e[1] || (e[1] = t => l.selectedModel = t),
                        class: "form-select"
                    }, [
                        (d(!0), r(m, null,
                            v(l.apiModels[l.selectedApi], t => (
                                d(),
                                r("option", { value: t.value, key: t.value }, b(t.text), 9, w)
                            )),
                            128))
                    ], 512), [[c, l.selectedModel]])
                ])
            ]),
            s("div", H, [
                e[17] || (e[17] = s("h4", { class: "section-title" }, "模式选择 RAG", -1)),
                s("div", G, [
                    (d(!0), r(m, null,
                        v(l.modes, t => (
                            d(), r("label", { key: t.value }, [
                                a(s("input", {
                                    type: "radio",
                                    "onUpdate:modelValue": e[2] || (e[2] = u => {
                                        l.selectedMode = u;
                                        u === "expert" && n.load_embedding();
                                    }),
                                    value: t.value,
                                    onChange: e[3] || (e[3] = (...u) => n.toggleModeOptions && n.toggleModeOptions(...u))
                                }, null, 40, D), [[M, l.selectedMode]]),
                                s("span", null, b(t.label), 1)
                            ])
                        )),
                        128))
                ])
            ]),
            s("div", F, [
                a(s("div", S, [
                    s("label", null, [
                        a(s("input", {
                            type: "checkbox",
                            "onUpdate:modelValue": e[8] || (e[8] = t => l.graphRagEnabled = t)
                        }, null, 512), [[g, l.graphRagEnabled]]),
                        e[21] || (e[21] = s("span", null, "GraphRAG", -1))
                    ]),
                    s("label", null, [
                        e[22] || (e[22] = y(" 📁 上传文档 ")),
                        s("input", {
                            type: "file",
                            onChange: e[9] || (e[9] = (...t) => n.handleFileUpload && n.handleFileUpload(...t)),
                            multiple: "",
                            hidden: ""
                        }, null, 32)
                    ])
                ], 512), [[h, l.selectedMode === "custom"]])
            ]),

            s("label", { class: "button-group" }, [
                s("button", {
                    onClick: e[30] || (e[30] = (...t) => n.loadReport && n.loadReport(...t)),
                    id: "generate-btn",
                    class: "btn clear-btn",
                    style: "display: inline-block;"
                }, "加载分析报告", 512),
                s("button", {
                    id: "generating-btn",
                    class: "btn clear-btn",
                    style: "display: none;"
                }, "加载中", 512),
            ]),
            s("label", { class: "button-group" }, [
                s("button", {
                    onClick: e[31] || (e[31] = (...t) => n.downloadReport && n.downloadReport(...t)),
                    id: "download-btn",
                    class: "btn clear-btn",
                    style: "display: none;"
                }, "下载报告", 512)
            ]),
            s("label", null, [
                s("button", {
                    onClick: e[10] || (e[10] = (...t) => n.clearHistory && n.clearHistory(...t)),
                    class: "btn clear-btn"
                }, "清除历史")
            ])
        ], 512),
        s("div", T, [
            s("div", O, [
                (d(!0), r(m, null,
                    v(l.messages, (t, u) => (
                        d(), r("div", {
                            key: u,
                            class: f(["chat-message", t.role])
                        }, b(t.content), 3)
                    )),
                    128))
            ], 512),
            s("div", B, [
                a(s("input", {
                    "onUpdate:modelValue": e[11] || (e[11] = t => l.inputMessage = t),
                    onKeyup: e[12] || (e[12] = k((...t) => n.sendMessage && n.sendMessage(...t), ["enter"])),
                    class: "chat-input",
                    placeholder: "输入你的问题..."
                }, null, 544), [[x, l.inputMessage]]),
                s("button", {
                    onClick: e[13] || (e[13] = (...t) => n.sendMessage && n.sendMessage(...t)),
                    class: "btn send-btn"
                }, e[23] || (e[23] = [
                    s("span", { class: "btn-content" }, "发送", -1)
                ]))
            ])
        ])
    ]);
}

const z = E(R, [["render", I], ["__scopeId", "data-v-b9051ea1"]]);
export { z as default };