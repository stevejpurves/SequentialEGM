import{c as L,i as c,j as v,k as l,m as g,p as E}from"/SequentialEGM/build/_shared/chunk-RMYRWJKG.js";var N=L((_,u)=>{c();v();l();E();g();function M(b){var e="[ \\t\\f]*",o="[ \\t\\f]+",r=e+"[:=]"+e,t=o,s="("+r+"|"+t+")",n="([^\\\\\\W:= \\t\\f\\n]|\\\\.)+",a="([^\\\\:= \\t\\f\\n]|\\\\.)+",i={end:s,relevance:0,starts:{className:"string",end:/$/,relevance:0,contains:[{begin:"\\\\\\\\"},{begin:"\\\\\\n"}]}};return{name:".properties",case_insensitive:!0,illegal:/\S/,contains:[b.COMMENT("^\\s*[!#]","$"),{returnBegin:!0,variants:[{begin:n+r,relevance:1},{begin:n+t,relevance:0}],contains:[{className:"attr",begin:n,endsParent:!0,relevance:0}],starts:i},{begin:a+s,returnBegin:!0,relevance:0,contains:[{className:"meta",begin:a,endsParent:!0,relevance:0}],starts:i},{className:"attr",relevance:0,begin:a+e+"$"}]}}u.exports=M});export default N();
