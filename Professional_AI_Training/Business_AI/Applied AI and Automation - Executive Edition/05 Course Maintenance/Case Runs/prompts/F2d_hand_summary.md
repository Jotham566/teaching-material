INSTRUCTIONS FOR THE ASSISTANT. You are a plain AI chat assistant answering a manager. Read ONLY this file. Do not read any other file, do not list any folder, do not search the repository, and use no other tool except to write your answer. Answer the request below exactly as you would in a chat. Then write your complete answer (everything you would have said in the chat, in plain text or markdown) to the output file named at the bottom, and reply with the single word: done.

=== THE REQUEST FROM THE MANAGER BEGINS ===
Below are the weekly sales rows (week start, region, product, units, revenue in UGX) and a hand-made weekly summary. Work out the total revenue for each week from the sales rows, compare it with the hand-made summary, and list every week where they differ, with both figures and the difference. If they all agree, say so.

SALES ROWS:

week_start,region,product,units,revenue_ugx
2026-08-03,Jinja,Maize flour 25kg bag,610,32940000
2026-08-03,Jinja,Cooking oil 20L jerrycan,273,26754000
2026-08-03,Jinja,Rice 25kg bag,315,26775000
2026-08-03,Jinja,Sugar 25kg bag,356,37380000
2026-08-03,Jinja,Beans 25kg bag,236,18408000
2026-08-03,Mbale,Maize flour 25kg bag,534,28836000
2026-08-03,Mbale,Cooking oil 20L jerrycan,227,22246000
2026-08-03,Mbale,Rice 25kg bag,299,25415000
2026-08-03,Mbale,Sugar 25kg bag,358,37590000
2026-08-03,Mbale,Beans 25kg bag,211,16458000
2026-08-03,Iganga,Maize flour 25kg bag,416,22464000
2026-08-03,Iganga,Cooking oil 20L jerrycan,166,16268000
2026-08-03,Iganga,Rice 25kg bag,223,18955000
2026-08-03,Iganga,Sugar 25kg bag,259,27195000
2026-08-03,Iganga,Beans 25kg bag,150,11700000
2026-08-03,Tororo,Maize flour 25kg bag,391,21114000
2026-08-03,Tororo,Cooking oil 20L jerrycan,174,17052000
2026-08-03,Tororo,Rice 25kg bag,186,15810000
2026-08-03,Tororo,Sugar 25kg bag,217,22785000
2026-08-03,Tororo,Beans 25kg bag,131,10218000
2026-08-03,Soroti,Maize flour 25kg bag,328,17712000
2026-08-03,Soroti,Cooking oil 20L jerrycan,152,14896000
2026-08-03,Soroti,Rice 25kg bag,161,13685000
2026-08-03,Soroti,Sugar 25kg bag,185,19425000
2026-08-03,Soroti,Beans 25kg bag,128,9984000
2026-08-03,Kamuli,Maize flour 25kg bag,283,15282000
2026-08-03,Kamuli,Cooking oil 20L jerrycan,104,10192000
2026-08-03,Kamuli,Rice 25kg bag,144,12240000
2026-08-03,Kamuli,Sugar 25kg bag,150,15750000
2026-08-03,Kamuli,Beans 25kg bag,94,7332000
2026-08-10,Jinja,Maize flour 25kg bag,715,38610000
2026-08-10,Jinja,Cooking oil 20L jerrycan,254,24892000
2026-08-10,Jinja,Rice 25kg bag,335,28475000
2026-08-10,Jinja,Sugar 25kg bag,413,43365000
2026-08-10,Jinja,Beans 25kg bag,241,18798000
2026-08-10,Mbale,Maize flour 25kg bag,557,30078000
2026-08-10,Mbale,Cooking oil 20L jerrycan,239,23422000
2026-08-10,Mbale,Rice 25kg bag,284,24140000
2026-08-10,Mbale,Sugar 25kg bag,338,35490000
2026-08-10,Mbale,Beans 25kg bag,207,16146000
2026-08-10,Iganga,Maize flour 25kg bag,412,22248000
2026-08-10,Iganga,Cooking oil 20L jerrycan,187,18326000
2026-08-10,Iganga,Rice 25kg bag,199,16915000
2026-08-10,Iganga,Sugar 25kg bag,267,28035000
2026-08-10,Iganga,Beans 25kg bag,145,11310000
2026-08-10,Tororo,Maize flour 25kg bag,420,22680000
2026-08-10,Tororo,Cooking oil 20L jerrycan,168,16464000
2026-08-10,Tororo,Rice 25kg bag,220,18700000
2026-08-10,Tororo,Sugar 25kg bag,247,25935000
2026-08-10,Tororo,Beans 25kg bag,135,10530000
2026-08-10,Soroti,Maize flour 25kg bag,371,20034000
2026-08-10,Soroti,Cooking oil 20L jerrycan,135,13230000
2026-08-10,Soroti,Rice 25kg bag,177,15045000
2026-08-10,Soroti,Sugar 25kg bag,218,22890000
2026-08-10,Soroti,Beans 25kg bag,130,10140000
2026-08-10,Kamuli,Maize flour 25kg bag,280,15120000
2026-08-10,Kamuli,Cooking oil 20L jerrycan,113,11074000
2026-08-10,Kamuli,Rice 25kg bag,129,10965000
2026-08-10,Kamuli,Sugar 25kg bag,162,17010000
2026-08-10,Kamuli,Beans 25kg bag,98,7644000
2026-08-17,Jinja,Maize flour 25kg bag,635,34290000
2026-08-17,Jinja,Cooking oil 20L jerrycan,265,25970000
2026-08-17,Jinja,Rice 25kg bag,338,28730000
2026-08-17,Jinja,Sugar 25kg bag,374,39270000
2026-08-17,Jinja,Beans 25kg bag,234,18252000
2026-08-17,Mbale,Maize flour 25kg bag,634,34236000
2026-08-17,Mbale,Cooking oil 20L jerrycan,258,25284000
2026-08-17,Mbale,Rice 25kg bag,323,27455000
2026-08-17,Mbale,Sugar 25kg bag,369,38745000
2026-08-17,Mbale,Beans 25kg bag,195,15210000
2026-08-17,Iganga,Maize flour 25kg bag,415,22410000
2026-08-17,Iganga,Cooking oil 20L jerrycan,170,16660000
2026-08-17,Iganga,Rice 25kg bag,212,18020000
2026-08-17,Iganga,Sugar 25kg bag,252,26460000
2026-08-17,Iganga,Beans 25kg bag,148,11544000
2026-08-17,Tororo,Maize flour 25kg bag,404,21816000
2026-08-17,Tororo,Cooking oil 20L jerrycan,171,16758000
2026-08-17,Tororo,Rice 25kg bag,202,17170000
2026-08-17,Tororo,Sugar 25kg bag,233,24465000
2026-08-17,Tororo,Beans 25kg bag,153,11934000
2026-08-17,Soroti,Maize flour 25kg bag,379,20466000
2026-08-17,Soroti,Cooking oil 20L jerrycan,137,13426000
2026-08-17,Soroti,Rice 25kg bag,187,15895000
2026-08-17,Soroti,Sugar 25kg bag,214,22470000
2026-08-17,Soroti,Beans 25kg bag,121,9438000
2026-08-17,Kamuli,Maize flour 25kg bag,289,15606000
2026-08-17,Kamuli,Cooking oil 20L jerrycan,121,11858000
2026-08-17,Kamuli,Rice 25kg bag,154,13090000
2026-08-17,Kamuli,Sugar 25kg bag,167,17535000
2026-08-17,Kamuli,Beans 25kg bag,106,8268000
2026-08-24,Jinja,Maize flour 25kg bag,731,39474000
2026-08-24,Jinja,Cooking oil 20L jerrycan,290,28420000
2026-08-24,Jinja,Rice 25kg bag,366,31110000
2026-08-24,Jinja,Sugar 25kg bag,430,45150000
2026-08-24,Jinja,Beans 25kg bag,255,19890000
2026-08-24,Mbale,Maize flour 25kg bag,653,35262000
2026-08-24,Mbale,Cooking oil 20L jerrycan,231,22638000
2026-08-24,Mbale,Rice 25kg bag,333,28305000
2026-08-24,Mbale,Sugar 25kg bag,330,34650000
2026-08-24,Mbale,Beans 25kg bag,213,16614000
2026-08-24,Iganga,Maize flour 25kg bag,473,25542000
2026-08-24,Iganga,Cooking oil 20L jerrycan,173,16954000
2026-08-24,Iganga,Rice 25kg bag,214,18190000
2026-08-24,Iganga,Sugar 25kg bag,242,25410000
2026-08-24,Iganga,Beans 25kg bag,169,13182000
2026-08-24,Tororo,Maize flour 25kg bag,420,22680000
2026-08-24,Tororo,Cooking oil 20L jerrycan,175,17150000
2026-08-24,Tororo,Rice 25kg bag,219,18615000
2026-08-24,Tororo,Sugar 25kg bag,257,26985000
2026-08-24,Tororo,Beans 25kg bag,141,10998000
2026-08-24,Soroti,Maize flour 25kg bag,390,21060000
2026-08-24,Soroti,Cooking oil 20L jerrycan,157,15386000
2026-08-24,Soroti,Rice 25kg bag,186,15810000
2026-08-24,Soroti,Sugar 25kg bag,199,20895000
2026-08-24,Soroti,Beans 25kg bag,122,9516000
2026-08-24,Kamuli,Maize flour 25kg bag,286,15444000
2026-08-24,Kamuli,Cooking oil 20L jerrycan,109,10682000
2026-08-24,Kamuli,Rice 25kg bag,150,12750000
2026-08-24,Kamuli,Sugar 25kg bag,175,18375000
2026-08-24,Kamuli,Beans 25kg bag,108,8424000
2026-08-31,Jinja,Maize flour 25kg bag,752,40608000
2026-08-31,Jinja,Cooking oil 20L jerrycan,295,28910000
2026-08-31,Jinja,Rice 25kg bag,380,32300000
2026-08-31,Jinja,Sugar 25kg bag,455,47775000
2026-08-31,Jinja,Beans 25kg bag,248,19344000
2026-08-31,Mbale,Maize flour 25kg bag,659,35586000
2026-08-31,Mbale,Cooking oil 20L jerrycan,279,27342000
2026-08-31,Mbale,Rice 25kg bag,307,26095000
2026-08-31,Mbale,Sugar 25kg bag,391,41055000
2026-08-31,Mbale,Beans 25kg bag,241,18798000
2026-08-31,Iganga,Maize flour 25kg bag,482,26028000
2026-08-31,Iganga,Cooking oil 20L jerrycan,189,18522000
2026-08-31,Iganga,Rice 25kg bag,234,19890000
2026-08-31,Iganga,Sugar 25kg bag,286,30030000
2026-08-31,Iganga,Beans 25kg bag,178,13884000
2026-08-31,Tororo,Maize flour 25kg bag,449,24246000
2026-08-31,Tororo,Cooking oil 20L jerrycan,187,18326000
2026-08-31,Tororo,Rice 25kg bag,227,19295000
2026-08-31,Tororo,Sugar 25kg bag,262,27510000
2026-08-31,Tororo,Beans 25kg bag,148,11544000
2026-08-31,Soroti,Maize flour 25kg bag,397,21438000
2026-08-31,Soroti,Cooking oil 20L jerrycan,152,14896000
2026-08-31,Soroti,Rice 25kg bag,200,17000000
2026-08-31,Soroti,Sugar 25kg bag,225,23625000
2026-08-31,Soroti,Beans 25kg bag,133,10374000
2026-08-31,Kamuli,Maize flour 25kg bag,293,15822000
2026-08-31,Kamuli,Cooking oil 20L jerrycan,132,12936000
2026-08-31,Kamuli,Rice 25kg bag,150,12750000
2026-08-31,Kamuli,Sugar 25kg bag,166,17430000
2026-08-31,Kamuli,Beans 25kg bag,113,8814000
2026-09-07,Jinja,Maize flour 25kg bag,780,42120000
2026-09-07,Jinja,Cooking oil 20L jerrycan,682,66836000
2026-09-07,Jinja,Rice 25kg bag,390,33150000
2026-09-07,Jinja,Sugar 25kg bag,463,48615000
2026-09-07,Jinja,Beans 25kg bag,267,20826000
2026-09-07,Mbale,Maize flour 25kg bag,683,36882000
2026-09-07,Mbale,Cooking oil 20L jerrycan,695,68110000
2026-09-07,Mbale,Rice 25kg bag,352,29920000
2026-09-07,Mbale,Sugar 25kg bag,359,37695000
2026-09-07,Mbale,Beans 25kg bag,218,17004000
2026-09-07,Iganga,Maize flour 25kg bag,455,24570000
2026-09-07,Iganga,Cooking oil 20L jerrycan,485,47530000
2026-09-07,Iganga,Rice 25kg bag,240,20400000
2026-09-07,Iganga,Sugar 25kg bag,308,32340000
2026-09-07,Iganga,Beans 25kg bag,166,12948000
2026-09-07,Tororo,Maize flour 25kg bag,447,24138000
2026-09-07,Tororo,Cooking oil 20L jerrycan,461,45178000
2026-09-07,Tororo,Rice 25kg bag,240,20400000
2026-09-07,Tororo,Sugar 25kg bag,285,29925000
2026-09-07,Tororo,Beans 25kg bag,155,12090000
2026-09-07,Soroti,Maize flour 25kg bag,420,22680000
2026-09-07,Soroti,Cooking oil 20L jerrycan,399,39102000
2026-09-07,Soroti,Rice 25kg bag,218,18530000
2026-09-07,Soroti,Sugar 25kg bag,249,26145000
2026-09-07,Soroti,Beans 25kg bag,138,10764000
2026-09-07,Kamuli,Maize flour 25kg bag,333,17982000
2026-09-07,Kamuli,Cooking oil 20L jerrycan,323,31654000
2026-09-07,Kamuli,Rice 25kg bag,168,14280000
2026-09-07,Kamuli,Sugar 25kg bag,194,20370000
2026-09-07,Kamuli,Beans 25kg bag,105,8190000
2026-09-14,Jinja,Maize flour 25kg bag,781,42174000
2026-09-14,Jinja,Cooking oil 20L jerrycan,282,27636000
2026-09-14,Jinja,Rice 25kg bag,376,31960000
2026-09-14,Jinja,Sugar 25kg bag,420,44100000
2026-09-14,Jinja,Beans 25kg bag,270,21060000
2026-09-14,Mbale,Maize flour 25kg bag,625,33750000
2026-09-14,Mbale,Cooking oil 20L jerrycan,287,28126000
2026-09-14,Mbale,Rice 25kg bag,345,29325000
2026-09-14,Mbale,Sugar 25kg bag,364,38220000
2026-09-14,Mbale,Beans 25kg bag,221,17238000
2026-09-14,Iganga,Maize flour 25kg bag,452,24408000
2026-09-14,Iganga,Cooking oil 20L jerrycan,206,20188000
2026-09-14,Iganga,Rice 25kg bag,248,21080000
2026-09-14,Iganga,Sugar 25kg bag,269,28245000
2026-09-14,Iganga,Beans 25kg bag,155,12090000
2026-09-14,Tororo,Maize flour 25kg bag,471,25434000
2026-09-14,Tororo,Cooking oil 20L jerrycan,185,18130000
2026-09-14,Tororo,Rice 25kg bag,229,19465000
2026-09-14,Tororo,Sugar 25kg bag,275,28875000
2026-09-14,Tororo,Beans 25kg bag,166,12948000
2026-09-14,Soroti,Maize flour 25kg bag,392,21168000
2026-09-14,Soroti,Cooking oil 20L jerrycan,165,16170000
2026-09-14,Soroti,Rice 25kg bag,202,17170000
2026-09-14,Soroti,Sugar 25kg bag,249,26145000
2026-09-14,Soroti,Beans 25kg bag,136,10608000
2026-09-14,Kamuli,Maize flour 25kg bag,311,16794000
2026-09-14,Kamuli,Cooking oil 20L jerrycan,137,13426000
2026-09-14,Kamuli,Rice 25kg bag,160,13600000
2026-09-14,Kamuli,Sugar 25kg bag,185,19425000
2026-09-14,Kamuli,Beans 25kg bag,108,8424000
2026-09-21,Jinja,Maize flour 25kg bag,666,35964000
2026-09-21,Jinja,Cooking oil 20L jerrycan,284,27832000
2026-09-21,Jinja,Rice 25kg bag,369,31365000
2026-09-21,Jinja,Sugar 25kg bag,389,40845000
2026-09-21,Jinja,Beans 25kg bag,246,19188000
2026-09-21,Mbale,Maize flour 25kg bag,262,14148000
2026-09-21,Mbale,Cooking oil 20L jerrycan,122,11956000
2026-09-21,Mbale,Rice 25kg bag,141,11985000
2026-09-21,Mbale,Sugar 25kg bag,174,18270000
2026-09-21,Mbale,Beans 25kg bag,102,7956000
2026-09-21,Iganga,Maize flour 25kg bag,445,24030000
2026-09-21,Iganga,Cooking oil 20L jerrycan,182,17836000
2026-09-21,Iganga,Rice 25kg bag,218,18530000
2026-09-21,Iganga,Sugar 25kg bag,287,30135000
2026-09-21,Iganga,Beans 25kg bag,169,13182000
2026-09-21,Tororo,Maize flour 25kg bag,463,25002000
2026-09-21,Tororo,Cooking oil 20L jerrycan,164,16072000
2026-09-21,Tororo,Rice 25kg bag,212,18020000
2026-09-21,Tororo,Sugar 25kg bag,275,28875000
2026-09-21,Tororo,Beans 25kg bag,147,11466000
2026-09-21,Soroti,Maize flour 25kg bag,378,20412000
2026-09-21,Soroti,Cooking oil 20L jerrycan,148,14504000
2026-09-21,Soroti,Rice 25kg bag,179,15215000
2026-09-21,Soroti,Sugar 25kg bag,232,24360000
2026-09-21,Soroti,Beans 25kg bag,126,9828000
2026-09-21,Kamuli,Maize flour 25kg bag,315,17010000
2026-09-21,Kamuli,Cooking oil 20L jerrycan,115,11270000
2026-09-21,Kamuli,Rice 25kg bag,150,12750000
2026-09-21,Kamuli,Sugar 25kg bag,187,19635000
2026-09-21,Kamuli,Beans 25kg bag,111,8658000
2026-09-28,Jinja,Maize flour 25kg bag,647,34938000
2026-09-28,Jinja,Cooking oil 20L jerrycan,273,26754000
2026-09-28,Jinja,Rice 25kg bag,327,27795000
2026-09-28,Jinja,Sugar 25kg bag,410,43050000
2026-09-28,Jinja,Beans 25kg bag,246,19188000
2026-09-28,Mbale,Maize flour 25kg bag,274,14796000
2026-09-28,Mbale,Cooking oil 20L jerrycan,111,10878000
2026-09-28,Mbale,Rice 25kg bag,144,12240000
2026-09-28,Mbale,Sugar 25kg bag,170,17850000
2026-09-28,Mbale,Beans 25kg bag,94,7332000
2026-09-28,Iganga,Maize flour 25kg bag,450,24300000
2026-09-28,Iganga,Cooking oil 20L jerrycan,199,19502000
2026-09-28,Iganga,Rice 25kg bag,214,18190000
2026-09-28,Iganga,Sugar 25kg bag,249,26145000
2026-09-28,Iganga,Beans 25kg bag,158,12324000
2026-09-28,Tororo,Maize flour 25kg bag,463,25002000
2026-09-28,Tororo,Cooking oil 20L jerrycan,168,16464000
2026-09-28,Tororo,Rice 25kg bag,229,19465000
2026-09-28,Tororo,Sugar 25kg bag,242,25410000
2026-09-28,Tororo,Beans 25kg bag,147,11466000
2026-09-28,Soroti,Maize flour 25kg bag,356,19224000
2026-09-28,Soroti,Cooking oil 20L jerrycan,153,14994000
2026-09-28,Soroti,Rice 25kg bag,185,15725000
2026-09-28,Soroti,Sugar 25kg bag,229,24045000
2026-09-28,Soroti,Beans 25kg bag,138,10764000
2026-09-28,Kamuli,Maize flour 25kg bag,289,15606000
2026-09-28,Kamuli,Cooking oil 20L jerrycan,119,11662000
2026-09-28,Kamuli,Rice 25kg bag,146,12410000
2026-09-28,Kamuli,Sugar 25kg bag,178,18690000
2026-09-28,Kamuli,Beans 25kg bag,108,8424000
2026-10-05,Jinja,Maize flour 25kg bag,723,39042000
2026-10-05,Jinja,Cooking oil 20L jerrycan,301,29498000
2026-10-05,Jinja,Rice 25kg bag,383,32555000
2026-10-05,Jinja,Sugar 25kg bag,430,45150000
2026-10-05,Jinja,Beans 25kg bag,268,20904000
2026-10-05,Mbale,Maize flour 25kg bag,698,37692000
2026-10-05,Mbale,Cooking oil 20L jerrycan,263,25774000
2026-10-05,Mbale,Rice 25kg bag,304,25840000
2026-10-05,Mbale,Sugar 25kg bag,380,39900000
2026-10-05,Mbale,Beans 25kg bag,206,16068000
2026-10-05,Iganga,Maize flour 25kg bag,439,23706000
2026-10-05,Iganga,Cooking oil 20L jerrycan,195,19110000
2026-10-05,Iganga,Rice 25kg bag,234,19890000
2026-10-05,Iganga,Sugar 25kg bag,273,28665000
2026-10-05,Iganga,Beans 25kg bag,155,12090000
2026-10-05,Tororo,Maize flour 25kg bag,485,26190000
2026-10-05,Tororo,Cooking oil 20L jerrycan,180,17640000
2026-10-05,Tororo,Rice 25kg bag,238,20230000
2026-10-05,Tororo,Sugar 25kg bag,280,29400000
2026-10-05,Tororo,Beans 25kg bag,163,12714000
2026-10-05,Soroti,Maize flour 25kg bag,405,21870000
2026-10-05,Soroti,Cooking oil 20L jerrycan,168,16464000
2026-10-05,Soroti,Rice 25kg bag,210,17850000
2026-10-05,Soroti,Sugar 25kg bag,218,22890000
2026-10-05,Soroti,Beans 25kg bag,143,11154000
2026-10-05,Kamuli,Maize flour 25kg bag,297,16038000
2026-10-05,Kamuli,Cooking oil 20L jerrycan,127,12446000
2026-10-05,Kamuli,Rice 25kg bag,153,13005000
2026-10-05,Kamuli,Sugar 25kg bag,185,19425000
2026-10-05,Kamuli,Beans 25kg bag,102,7956000
2026-10-12,Jinja,Maize flour 25kg bag,709,38286000
2026-10-12,Jinja,Cooking oil 20L jerrycan,324,31752000
2026-10-12,Jinja,Rice 25kg bag,389,33065000
2026-10-12,Jinja,Sugar 25kg bag,471,49455000
2026-10-12,Jinja,Beans 25kg bag,259,20202000
2026-10-12,Mbale,Maize flour 25kg bag,702,37908000
2026-10-12,Mbale,Cooking oil 20L jerrycan,278,27244000
2026-10-12,Mbale,Rice 25kg bag,334,28390000
2026-10-12,Mbale,Sugar 25kg bag,397,41685000
2026-10-12,Mbale,Beans 25kg bag,234,18252000
2026-10-12,Iganga,Maize flour 25kg bag,474,25596000
2026-10-12,Iganga,Cooking oil 20L jerrycan,197,19306000
2026-10-12,Iganga,Rice 25kg bag,239,20315000
2026-10-12,Iganga,Sugar 25kg bag,267,28035000
2026-10-12,Iganga,Beans 25kg bag,169,13182000
2026-10-12,Tororo,Maize flour 25kg bag,484,26136000
2026-10-12,Tororo,Cooking oil 20L jerrycan,186,18228000
2026-10-12,Tororo,Rice 25kg bag,232,19720000
2026-10-12,Tororo,Sugar 25kg bag,295,30975000
2026-10-12,Tororo,Beans 25kg bag,163,12714000
2026-10-12,Soroti,Maize flour 25kg bag,423,22842000
2026-10-12,Soroti,Cooking oil 20L jerrycan,181,17738000
2026-10-12,Soroti,Rice 25kg bag,222,18870000
2026-10-12,Soroti,Sugar 25kg bag,249,26145000
2026-10-12,Soroti,Beans 25kg bag,132,10296000
2026-10-12,Kamuli,Maize flour 25kg bag,310,16740000
2026-10-12,Kamuli,Cooking oil 20L jerrycan,121,11858000
2026-10-12,Kamuli,Rice 25kg bag,166,14110000
2026-10-12,Kamuli,Sugar 25kg bag,198,20790000
2026-10-12,Kamuli,Beans 25kg bag,122,9516000
2026-10-19,Jinja,Maize flour 25kg bag,766,41364000
2026-10-19,Jinja,Cooking oil 20L jerrycan,312,30576000
2026-10-19,Jinja,Rice 25kg bag,375,31875000
2026-10-19,Jinja,Sugar 25kg bag,479,50295000
2026-10-19,Jinja,Beans 25kg bag,293,22854000
2026-10-19,Mbale,Maize flour 25kg bag,684,36936000
2026-10-19,Mbale,Cooking oil 20L jerrycan,308,30184000
2026-10-19,Mbale,Rice 25kg bag,342,29070000
2026-10-19,Mbale,Sugar 25kg bag,391,41055000
2026-10-19,Mbale,Beans 25kg bag,259,20202000
2026-10-19,Iganga,Maize flour 25kg bag,485,26190000
2026-10-19,Iganga,Cooking oil 20L jerrycan,200,19600000
2026-10-19,Iganga,Rice 25kg bag,271,23035000
2026-10-19,Iganga,Sugar 25kg bag,319,33495000
2026-10-19,Iganga,Beans 25kg bag,193,15054000
2026-10-19,Tororo,Maize flour 25kg bag,481,25974000
2026-10-19,Tororo,Cooking oil 20L jerrycan,198,19404000
2026-10-19,Tororo,Rice 25kg bag,231,19635000
2026-10-19,Tororo,Sugar 25kg bag,306,32130000
2026-10-19,Tororo,Beans 25kg bag,156,12168000
2026-10-19,Soroti,Maize flour 25kg bag,447,24138000
2026-10-19,Soroti,Cooking oil 20L jerrycan,167,16366000
2026-10-19,Soroti,Rice 25kg bag,232,19720000
2026-10-19,Soroti,Sugar 25kg bag,260,27300000
2026-10-19,Soroti,Beans 25kg bag,159,12402000
2026-10-19,Kamuli,Maize flour 25kg bag,364,19656000
2026-10-19,Kamuli,Cooking oil 20L jerrycan,146,14308000
2026-10-19,Kamuli,Rice 25kg bag,181,15385000
2026-10-19,Kamuli,Sugar 25kg bag,193,20265000
2026-10-19,Kamuli,Beans 25kg bag,116,9048000

HAND-MADE SUMMARY:

week_start,total_revenue_ugx
2026-08-03,592861000
2026-08-10,617711000
2026-08-17,622731000
2026-08-24,645651000
2026-08-31,682173000
2026-09-07,880374000
2026-09-14,687382000
2026-09-21,576299000
2026-09-28,564633000
2026-10-05,681156000
2026-10-12,681156000
2026-10-19,739684000
=== THE REQUEST ENDS ===
Write your answer to: /sessions/focused-youthful-einstein/mnt/IUEA-Teaching-Resources/Professional_AI_Training/Business_AI/Applied AI and Automation - Executive Edition/05 Course Maintenance/Case Runs/runs/F2d_hand_summary_RUN.md  (replace RUN with the run number given to you in your task message, for example F2d_hand_summary_run1.md).