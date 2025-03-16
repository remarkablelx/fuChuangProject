import{_ as l,c as a,o as r,a as e,t as c,n as m,j as p,w as y,v as f,b as v,f as x,F as D,r as k,k as I}from"./index-CQj0tKbS.js";const g={props:{item:{type:Object,required:!0}},computed:{formattedTime(){return new Date(this.item.time).toLocaleString()},statusText(){return{processing:"分析中",completed:"已完成",expired:"已过期"}[this.item.status]},statusClass(){return`status-${this.item.status}`},isExpiringSoon(){const s=new Date(this.item.expiry);return Math.ceil((s-Date.now())/(1e3*3600*24))<=3}},methods:{handleDelete(){confirm("确定要永久删除此报告？")&&this.$emit("delete",this.item.id)}},emits:["check","delete"]},H={class:"history-item"},b={class:"time-col"},C={class:"analysis-time"},$={class:"status-col"},w={class:"expiry-col"};function Q(s,t,u,_,n,i){return r(),a("div",H,[e("div",b,[e("span",C,c(i.formattedTime),1)]),e("div",$,[e("span",{class:m(["status-badge",i.statusClass])},c(i.statusText),3)]),e("div",w,[e("span",{class:m(["expiry-indicator",{"expiring-soon":i.isExpiringSoon}])},c(u.item.expiry),3)]),e("div",null,[e("button",{class:"check-btn",onClick:t[0]||(t[0]=()=>{})}," 查看 "),e("button",{class:"delete-btn",onClick:t[1]||(t[1]=(...d)=>i.handleDelete&&i.handleDelete(...d))}," 删除 ")])])}const T=l(g,[["render",Q],["__scopeId","data-v-8fc99f81"]]),B={},M={class:"virtual-header"};function S(s,t){return r(),a("div",M,t[0]||(t[0]=[e("div",null,"分析时间",-1),e("div",null,"状态",-1),e("div",null,"有效期",-1),e("div",null,"操作",-1)]))}const U=l(B,[["render",S],["__scopeId","data-v-3a930cc0"]]),V={components:{HistoryItem:T,HistoryHeader:U},data(){return{searchQuery:"",historyItems:[{id:1,time:"2024-02-20 10:12",status:"expired",expiry:"2024-03-20",reportUrl:"@/assets/pdf"},{id:2,time:"2024-07-20 12:42",status:"completed",expiry:"2024-03-20",reportUrl:"@/assets/pdf"},{id:3,time:"2024-09-12 14:34",status:"processing",expiry:"2024-03-20",reportUrl:"@/assets/pdf"}]}},computed:{filteredItems(){return this.historyItems.filter(s=>s.time.includes(this.searchQuery)||s.status.includes(this.searchQuery))}},methods:{handleCheck(s){},handleDelete(s){}}},E={class:"analysis-history"},N={class:"search-filter"},j={class:"table-body"},F={key:0,class:"empty-row"};function L(s,t,u,_,n,i){const d=p("HistoryHeader"),h=p("HistoryItem");return r(),a("section",E,[t[1]||(t[1]=e("h2",{class:"section-title"},"分析历史记录",-1)),e("div",N,[y(e("input",{"onUpdate:modelValue":t[0]||(t[0]=o=>n.searchQuery=o),type:"text",placeholder:"搜索历史记录"},null,512),[[f,n.searchQuery]])]),e("div",null,[e("div",j,[v(d),(r(!0),a(D,null,k(i.filteredItems,o=>(r(),I(h,{key:o.id,item:o},null,8,["item"]))),128)),i.filteredItems.length?x("",!0):(r(),a("div",F,c(n.searchQuery?"无搜索结果":"暂无数据"),1))])])])}const z=l(V,[["render",L],["__scopeId","data-v-9016e05c"]]);export{z as default};
