import{i as g,k as c,_ as u,o as p,c as m,b as t,t as r,w as l,f as n,v as d,n as h,g as w,p as f,m as _}from"./index-ovc9-s1E.js";import{V as y}from"./common-u2_REoPp.js";import{_ as b}from"./logoPrincipal-owaQzuwk.js";function v(){return{showMessage:!1,message:"",typeMessage:""}}const M={name:"Home",data(){return{password:"",password_confirmation:"",errors:[],type_message:"info",message:v(),app_version:g("app_version")}},mounted(){document.title="Detect One";const s=document.querySelector("body");s&&s.setAttribute("class","login-style")},methods:{preGeneratePassword(){this.errors=y.savePassword(this.password,this.password_confirmation),this.errors.length==0?this.generatePassword():(this.message.message=this.errors[0],this.message.typeMessage="info-error")},generatePassword(){const s=new FormData;s.set("password",this.password),s.set("email",this.$route.params.email),s.set("token",this.$route.params.token),c.post("/api/management/generate_password/",s).then(e=>{this.message.showMessage=!0,e.status==406?this.message.typeMessage="info-error":this.message.typeMessage="info",this.message.message=e.data.message}).catch(e=>{e.response.data&&(this.message.message=e.response.data.message,this.message.showMessage=!0,this.message.typeMessage="info-error")})},goLogin(){this.$router.push({name:"Login"})}}},k=s=>(f("data-v-e74d2082"),s=s(),_(),s),P={class:"home"},S={id:"login"},V={class:"login-white-square medium_square"},I={class:"info_version"},x=k(()=>t("div",{class:"logo_sia"},[t("img",{src:b,alt:"SIA",style:{width:"100%"}})],-1)),D={type:"submit",class:"btn login"},G={style:{"font-weight":"bold"}};function q(s,e,B,C,a,i){return p(),m("div",P,[t("section",S,[t("div",V,[t("div",I,[t("b",null,r(a.app_version),1)]),t("form",{onSubmit:e[4]||(e[4]=l((...o)=>i.preGeneratePassword&&i.preGeneratePassword(...o),["prevent"]))},[x,n(t("input",{class:"mt-0","onUpdate:modelValue":e[0]||(e[0]=o=>s.$route.params.email=o),placeholder:"Password",maxlength:"20",autocomplete:"off","aria-describedby":"password-feedback",disabled:"",style:{opacity:"0.5"},type:"text"},null,512),[[d,s.$route.params.email]]),n(t("input",{"onUpdate:modelValue":e[1]||(e[1]=o=>a.password=o),placeholder:"Password",maxlength:"20","aria-describedby":"password-feedback",type:"password"},null,512),[[d,a.password]]),n(t("input",{"onUpdate:modelValue":e[2]||(e[2]=o=>a.password_confirmation=o),placeholder:"Repeat password",maxlength:"20","aria-describedby":"password-feedback",type:"password"},null,512),[[d,a.password_confirmation]]),t("button",D,r(s.$t("send")),1),a.message.message?(p(),m("div",{key:0,class:h(a.message.typeMessage)},[t("p",G,r(s.$t(a.message.message)),1)],2)):w("",!0),t("span",{class:"select-pointer",onClick:e[3]||(e[3]=l(o=>i.goLogin(),["stop"]))},r(s.$t("go_to_login")),1)],32)])])])}const N=u(M,[["render",q],["__scopeId","data-v-e74d2082"]]);export{N as default};
