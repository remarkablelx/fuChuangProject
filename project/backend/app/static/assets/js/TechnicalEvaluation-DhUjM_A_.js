import{c as r,o as d,a as s,w as a,B as c,F as m,r as v,t as b,C as M,D as h,E as g,h as y,n as f,v as x,G as k}from"./index-DvFSEw6X.js";import{_ as E}from"./Logo-DoPk92ps.js";const R={data(){return{messages:[],inputMessage:"",selectedApi:"openai",selectedModel:"gpt-4o",selectedMode:"custom",selectedExpert:"Cybersecurity-RAG",graphRagEnabled:!0,apiModels:{openai:[{value:"gpt-4o",text:"gpt-4o"},{value:"gpt-3.5-turbo",text:"gpt-3.5-turbo"}],volcengine:[{value:"deepseek-r1",text:"deep-r1"},{value:"deepseek-v3",text:"deep-v3"}]},modes:[{value:"custom",label:"自定义"},{value:"expert",label:"专家"}]}},methods:{async sendMessage(){const o=this.inputMessage.trim();if(o){this.messages.push({role:"user",content:o}),this.inputMessage="";try{const e=await this.streamChatResponse({prompt:o,chatHistory:this.messages.slice(-5),mode:this.selectedMode,graphrag:this.graphRagEnabled,context:this.generateContext()});let i="";for await(const p of this.mockStream(e))i+=p,this.updateAssistantMessage(i)}catch(e){console.error("Error:",e),this.addMessage("assistant","抱歉，请求处理失败")}}},updateAssistantMessage(o){const e=this.messages[this.messages.length-1];(e==null?void 0:e.role)==="assistant"?e.content=o:this.messages.push({role:"assistant",content:o}),this.$nextTick(()=>{this.$refs.chatHistory.scrollTop=this.$refs.chatHistory.scrollHeight})},handleFileUpload(o){const e=Array.from(o.target.files),i=new FormData;e.forEach(p=>i.append("files",p)),console.log("Uploading files:",e)},clearHistory(){this.messages=[]},toggleModeOptions(){},generateContext(){return this.selectedMode==="expert"?"[专家文档内容示例]":"[自定义文档内容示例]"},async*mockStream(o){const e=o.split(" ");for(const i of e)yield new Promise(p=>setTimeout(()=>p(i+" "),50))}}},A={class:"chat-container"},U={class:"sidebar"},C={class:"bar-section model-section"},V={class:"select-group"},w=["value"],H={class:"bar-section mode-section"},G={class:"select-group"},D=["value"],F={class:"bar-section"},S={class:"select-group"},T={class:"chat-wrapper"},B={class:"chat-history",ref:"chatHistory"},O={class:"input-area"};function I(o,e,i,p,l,n){return d(),r("div",A,[s("aside",U,[s("div",C,[e[15]||(e[15]=s("h4",{class:"section-title"},"模型切换",-1)),s("div",V,[a(s("select",{"onUpdate:modelValue":e[0]||(e[0]=t=>l.selectedApi=t),class:"form-select"},e[14]||(e[14]=[s("option",{value:"openai"},"OpenAI",-1),s("option",{value:"volcengine"},"DeepSeek",-1)]),512),[[c,l.selectedApi]]),a(s("select",{"onUpdate:modelValue":e[1]||(e[1]=t=>l.selectedModel=t),class:"form-select"},[(d(!0),r(m,null,v(l.apiModels[l.selectedApi],t=>(d(),r("option",{value:t.value,key:t.value},b(t.text),9,w))),128))],512),[[c,l.selectedModel]])])]),s("div",H,[e[17]||(e[17]=s("h4",{class:"section-title"},"模式选择 RAG",-1)),s("div",G,[(d(!0),r(m,null,v(l.modes,t=>(d(),r("label",{key:t.value},[a(s("input",{type:"radio","onUpdate:modelValue":e[2]||(e[2]=u=>l.selectedMode=u),value:t.value,onChange:e[3]||(e[3]=(...u)=>n.toggleModeOptions&&n.toggleModeOptions(...u))},null,40,D),[[M,l.selectedMode]]),s("span",null,b(t.label),1)]))),128))]),a(s("select",{"onUpdate:modelValue":e[4]||(e[4]=t=>l.selectedExpert=t),class:"form-select expert-select"},e[16]||(e[16]=[s("option",{value:"Cybersecurity-RAG"},"网络安全",-1),s("option",{value:"Medical-RAG"},"医疗健康",-1)]),512),[[c,l.selectedExpert],[h,l.selectedMode==="expert"]])]),s("div",F,[a(s("div",S,[s("label",null,[a(s("input",{type:"checkbox","onUpdate:modelValue":e[5]||(e[5]=t=>l.graphRagEnabled=t)},null,512),[[g,l.graphRagEnabled]]),e[18]||(e[18]=s("span",null,"RAG",-1))]),s("label",null,[a(s("input",{type:"checkbox","onUpdate:modelValue":e[6]||(e[6]=t=>l.graphRagEnabled=t)},null,512),[[g,l.graphRagEnabled]]),e[19]||(e[19]=s("span",null,"HyDE",-1))]),s("label",null,[a(s("input",{type:"checkbox","onUpdate:modelValue":e[7]||(e[7]=t=>l.graphRagEnabled=t)},null,512),[[g,l.graphRagEnabled]]),e[20]||(e[20]=s("span",null,"Reranking",-1))]),s("label",null,[a(s("input",{type:"checkbox","onUpdate:modelValue":e[8]||(e[8]=t=>l.graphRagEnabled=t)},null,512),[[g,l.graphRagEnabled]]),e[21]||(e[21]=s("span",null,"GraphRAG",-1))]),s("label",null,[e[22]||(e[22]=y(" 📁 上传文档 ")),s("input",{type:"file",onChange:e[9]||(e[9]=(...t)=>n.handleFileUpload&&n.handleFileUpload(...t)),multiple:"",hidden:""},null,32)])],512),[[h,l.selectedMode==="custom"]])]),s("button",{onClick:e[10]||(e[10]=(...t)=>n.clearHistory&&n.clearHistory(...t)),class:"btn clear-btn"},"清除历史")]),s("div",T,[s("div",B,[(d(!0),r(m,null,v(l.messages,(t,u)=>(d(),r("div",{key:u,class:f(["chat-message",t.role])},b(t.content),3))),128))],512),s("div",O,[a(s("input",{"onUpdate:modelValue":e[11]||(e[11]=t=>l.inputMessage=t),onKeyup:e[12]||(e[12]=k((...t)=>n.sendMessage&&n.sendMessage(...t),["enter"])),class:"chat-input",placeholder:"输入你的问题..."},null,544),[[x,l.inputMessage]]),s("button",{onClick:e[13]||(e[13]=(...t)=>n.sendMessage&&n.sendMessage(...t)),class:"btn send-btn"},e[23]||(e[23]=[s("span",{class:"btn-content"},"发送",-1)]))])])])}const z=E(R,[["render",I],["__scopeId","data-v-b9051ea1"]]);export{z as default};
