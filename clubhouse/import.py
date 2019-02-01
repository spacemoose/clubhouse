import json

ghu_to_chu = {
    'chenny408':'paulchen408',
    'MaEtUgR':'maetugr',
    'simonegu':'simonegu',
    'Stifael':'stifael',
    'spacemoose':'spacemoose',
    'Joezhuchg':'joezhu',
    'potaito':'alessandro'
}
j =   json.dumps(ghu_to_chu)
f = open('/home/stark/repos/yuneec/user_mapping.json',"w")
f.write(j)
f.close()
