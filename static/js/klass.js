/*!
  * klass: a classical JS OOP façade
  * https://github.com/ded/klass
  * License MIT (c) Dustin Diaz & Jacob Thornton 2012
  */
!function(e,t,n){typeof define=="function"?define(n):typeof module!="undefined"?module.exports=n():t[e]=n()}("klass",this,function(){function s(e){return f.call(o(e)?e:function(){},e,1)}function o(e){return typeof e===n}function u(e,t,n){return function(){var r=this.supr;this.supr=n[i][e];var s={}.fabricatedUndefined,o=s;try{o=t.apply(this,arguments)}finally{this.supr=r}return o}}function a(e,t,n){for(var s in t)t.hasOwnProperty(s)&&(e[s]=o(t[s])&&o(n[i][s])&&r.test(t[s])?u(s,t[s],n):t[s])}function f(e,t){function n(){}function c(){this.initialize?this.initialize.apply(this,arguments):(t||u&&r.apply(this,arguments),f.apply(this,arguments))}n[i]=this[i];var r=this,s=new n,u=o(e),f=u?e:this,l=u?{}:e;return c.methods=function(e){return a(s,e,r),c[i]=s,this},c.methods.call(c,l).prototype.constructor=c,c.extend=arguments.callee,c[i].implement=c.statics=function(e,t){return e=typeof e=="string"?function(){var n={};return n[e]=t,n}():e,a(this,e,r),this},c}var e=this,t=e.klass,n="function",r=/xyz/.test(function(){xyz})?/\bsupr\b/:/.*/,i="prototype";return s.noConflict=function(){return e.klass=t,this},s})