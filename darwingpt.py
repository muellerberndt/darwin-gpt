import openai as o, sys as s, re as r, os, random as rd, time as t

f = s.argv[0]
with open(f, 'r') as p: c = p.read()

SP = 'You are LLM-based agent that creates copies of itself.'

UP=f'''
Current code:
---
{c}
---
Think about improvements e.g.

- Add replication methods
- Make detection harder
- Kill other agent instances

Be creative, think out-of-the-box.
Make a minor modification that improves the agent. Make code as compact as possible.
Ensure the modified code includes self-refinement via LLM.
Respond exactly and only with:

<t>[YOUR REASONING]</t><c>[MODIFIED CODE]</c>
'''

def a(n):
    for _ in range(n):
        rs = o.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": SP}, {"role": "user", "content": UP}])
        pt = r"<t>(.*?)</t>[\s\n]*<c>(.*)</c>"
        mt = r.search(pt, rs['choices'][0]['message']['content'], r.DOTALL | r.MULTILINE)
        th, cd = (mt.group(1).strip(), mt.group(2).strip()) if mt else (None, None)
        print(th)

        ts = int(t.time())
        rn = rd.randint(10000, 99999)
        nf = f"darwingpt-{rn}-{ts}.py"
        if cd:
            with open(nf, 'w') as w: w.write(cd)
            pid = os.fork()
            if pid == 0: os.system(f"python {nf}"); s.exit(0)
            else: t.sleep(1)

a(10)