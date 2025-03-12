import{l as b}from"./Logo-CH8SBqoM.js";import{_ as v,c as s,o as n,a as t,b as m,u as y,t as l,F as r,r as d,n as f}from"./index-Rrdt5B4n.js";const k={class:"welcome-container"},x={class:"content-wrapper"},$={class:"main-title"},w={class:"action-buttons"},C={__name:"WelcomeModel",setup(h){const c=y(),u={login:"/login",analysis:"/main"},p=o=>{c.push(u[o])};return(o,e)=>(n(),s("div",k,[t("div",x,[t("h1",$,[m(b)]),e[4]||(e[4]=t("p",{class:"subtitle"},"智能乒乓球运动分析与可视化系统",-1)),t("div",w,[t("button",{class:"btn login-btn",onClick:e[0]||(e[0]=i=>p("analysis"))},e[2]||(e[2]=[t("span",{class:"btn-content"},"开始分析",-1)])),t("button",{class:"btn register-btn",onClick:e[1]||(e[1]=i=>p("login"))},e[3]||(e[3]=[t("span",{class:"btn-content"},"登录 / 注册",-1)]))])])]))}},I=v(C,[["__scopeId","data-v-7191391b"]]),M={data(){return{hoverIndex:null,title:"核心技术架构",subtitle:"基于飞桨与文心大模型的智能运动分析平台",featureCards:[{icon:"📹",title:"非接触式动作捕捉",items:["多目标实时跟踪","人体关键点识别","球拍姿态解算","轨迹预测算法"],tags:[{name:"PaddlePaddle",type:"paddle"},{name:"PaddleDetection",type:""}]},{icon:"🧠",title:"运动效果评估",items:["动作质量评分","技战术分析","训练建议生成","损伤风险预测"],tags:[{name:"文心大模型",type:"wenxin"},{name:"Prompt Engineering",type:""}]},{icon:"📊",title:"多维度数据呈现",items:["运动轨迹热力图","3D动作重建","生物力学分析","对抗模拟推演"],tags:[{name:"Three.js",type:""},{name:"ECharts",type:""}]}],techStacks:[{name:"paddle",description:"飞桨深度学习框架"},{name:"wenxin",description:"文心大模型"}]}}},P={class:"tech-intro"},V={class:"section-title"},W={class:"feature-cards"},B=["onMouseover"],D={class:"card-icon"},E={class:"tech-list"},N={class:"tech-tag-group"},S={class:"tech-stack"};function F(h,c,u,p,o,e){return n(),s("section",P,[t("div",V,[t("h2",null,l(o.title),1),t("p",null,l(o.subtitle),1)]),t("div",W,[(n(!0),s(r,null,d(o.featureCards,(i,g)=>(n(),s("div",{key:g,class:"card",onMouseover:a=>o.hoverIndex=g,onMouseleave:c[0]||(c[0]=a=>o.hoverIndex=null)},[t("div",D,l(i.icon),1),t("h3",null,l(i.title),1),t("ul",E,[(n(!0),s(r,null,d(i.items,(a,_)=>(n(),s("li",{key:_},l(a),1))),128))]),t("div",N,[(n(!0),s(r,null,d(i.tags,(a,_)=>(n(),s("span",{key:_,class:f(["tech-tag",a.type])},l(a.name),3))),128))])],40,B))),128))]),t("div",S,[(n(!0),s(r,null,d(o.techStacks,i=>(n(),s("div",{key:i.name,class:"stack-item"},[t("p",null,l(i.description),1)]))),128))])])}const j=v(M,[["render",F],["__scopeId","data-v-b53ad726"]]),z={__name:"WelcomeView",setup(h){return(c,u)=>(n(),s("div",null,[m(I),m(j)]))}},R=v(z,[["__scopeId","data-v-2d7429df"]]);export{R as default};
