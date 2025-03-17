import re

def f(res):
    txt1=res.split("```")
    txt2=re.findall(r"```(.*?)```",res,re.DOTALL)
    if txt2==[]:
        res=res.strip('"')
        res=re.sub(r"<+",r'&lt;',res,flags=re.DOTALL)
        res=re.sub(r">+",r"&gt;",res,flags=re.DOTALL)
        res=re.sub(r"\*\*\s*(.*?)\s*\*\*", r" \1 ", res,flags=re.DOTALL)
        res=re.sub(r"\*(\S.*?)\*(?!\w)", r"  \1  ", res)
        res=re.sub(r"^\s*\*", r"•", res, flags=re.MULTILINE)
        res=re.sub(r"\\n", "\n", res,flags=re.DOTALL)
        res = re.sub(r"^\s*```(\w*)\n(.*?)\n\s*```$", r"<pre><code class='\1'>\2</code></pre>", res, flags=re.DOTALL | re.MULTILINE)
        res=re.sub(r"\`(.*?)\`", r"<code>\1</code>", res,flags=re.DOTALL)
        return res
    txt=''
    for i in txt1:
        if i in txt2:
            print("cod")
            i=re.sub(r"\\n", "\n", i,flags=re.DOTALL)
            i = re.sub(r"^.*\n", "", i, 1)
            i=re.sub(r"<+",r'&lt;',i,flags=re.DOTALL)
            i=re.sub(r">+",r"&gt;",i,flags=re.DOTALL)
            txt+=f"<pre>\n{i}\n</pre>"
        elif i:
            i=i.strip('"')
            i=re.sub(r"<+",r'&lt;',i,flags=re.DOTALL)
            i=re.sub(r">+",r"&gt;",i,flags=re.DOTALL)
            i=re.sub(r"\*\*\s*(.*?)\s*\*\*", r" \1 ", i,flags=re.DOTALL)
            i=re.sub(r"\*(\S.*?)\*(?!\w)", r" \1 ", i)
            i=re.sub(r"^\s*\*", r"•", i, flags=re.MULTILINE)
            i=re.sub(r"\\n", "\n", i,flags=re.DOTALL)
            i = re.sub(r"^\s*```(\w*)\n(.*?)\n\s*```$", r"<pre><code class='\1'>\2</code></pre>", i, flags=re.DOTALL | re.MULTILINE)
            i=re.sub(r"\`(.*?)\`", r"<code>\1</code>", i,flags=re.DOTALL)
            txt+=i
    return txt
