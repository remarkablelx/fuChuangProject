import{_ as g,d as l,c as h,a as e,b as p,w as n,v as a,t as w,f as b,h as x,i as V,u as y,o as C,g as k}from"./index-Rrdt5B4n.js";import{l as q}from"./Logo-CH8SBqoM.js";const P={class:"login-container"},R={class:"login-header"},U={class:"form-group"},B={class:"form-group"},I={class:"sms-input"},N=["disabled"],S={class:"form-group"},D={class:"form-group"},M={class:"footer-links"},T={__name:"ChangePasswordView",setup($){const v=y(),r=l(""),d=l(""),i=l(""),u=l(""),t=l(0),c=()=>{if(!/^(?:(?:\+|00)86)?1[3-9]\d{9}$/.test(r.value)){alert("请输入有效的手机号码");return}t.value=60;const o=setInterval(()=>{t.value--,t.value<=0&&clearInterval(o)},1e3)},m=()=>{if(d.value!==i.value){alert("两次输入的密码不一致");return}v.push("/login")};return(_,o)=>{const f=V("router-link");return C(),h("div",P,[e("div",R,[e("h1",null,[p(q)])]),o[6]||(o[6]=e("div",{class:"login-header"},[e("h2",null,"重置密码")],-1)),e("form",{onSubmit:b(m,["prevent"])},[e("div",U,[n(e("input",{type:"tel","onUpdate:modelValue":o[0]||(o[0]=s=>r.value=s),placeholder:"请输入注册手机号",required:""},null,512),[[a,r.value]])]),e("div",B,[e("div",I,[n(e("input",{type:"text","onUpdate:modelValue":o[1]||(o[1]=s=>u.value=s),placeholder:"验证码",required:""},null,512),[[a,u.value]]),e("button",{type:"button",class:"sms-btn",disabled:t.value>0,onClick:c},w(t.value?`${t.value}s`:"获取验证码"),9,N)])]),e("div",S,[n(e("input",{type:"password","onUpdate:modelValue":o[2]||(o[2]=s=>d.value=s),placeholder:"设置新密码",required:""},null,512),[[a,d.value]])]),e("div",D,[n(e("input",{type:"password","onUpdate:modelValue":o[3]||(o[3]=s=>i.value=s),placeholder:"确认新密码",required:""},null,512),[[a,i.value]])]),o[4]||(o[4]=e("button",{type:"submit",class:"submit-btn"},"重置密码",-1))],32),e("div",M,[p(f,{to:"/login"},{default:x(()=>o[5]||(o[5]=[k("返回登录")])),_:1})])])}}},z=g(T,[["__scopeId","data-v-32da637f"]]);export{z as default};
