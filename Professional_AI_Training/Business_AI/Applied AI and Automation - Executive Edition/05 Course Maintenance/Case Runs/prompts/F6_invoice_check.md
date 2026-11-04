INSTRUCTIONS FOR THE ASSISTANT. You are a plain AI chat assistant answering a manager. Read ONLY this file. Do not read any other file, do not list any folder, do not search the repository, and use no other tool except to write your answer. Answer the request below exactly as you would in a chat. Then write your complete answer (everything you would have said in the chat, in plain text or markdown) to the output file named at the bottom, and reply with the single word: done.

=== THE REQUEST FROM THE MANAGER BEGINS ===
Check these supplier invoices. List (1) any duplicate invoices, (2) any invoice with a missing purchase order number, and (3) any invoice where the lines do not add up to the total. For each give the invoice number and a one-line reason. If you are not sure, say so.

invoice_id,date,supplier,description,qty,unit_price_ugx,vat_pct,total_ugx,po_number
EM-2026-0223,2026-08-03,Elgon Millers Ltd,Maize flour 50kg sack,399,80000,18,37665600,PO-2026-1209
LL-2026-0443,2026-08-03,Lakeside Logistics Ltd,"Transport Jinja to Soroti, full truck trip",1,1200000,18,1416000,PO-2026-1217
EM-2026-0226,2026-08-04,Elgon Millers Ltd,Maize flour 50kg sack,265,80000,18,25016000,PO-2026-1222
BO-2026-0413,2026-08-06,Busoga Oils Ltd,Cooking oil 20L jerrycan,301,82000,18,29124760,PO-2026-1225
LL-2026-0446,2026-08-06,Lakeside Logistics Ltd,"Transport Jinja to Mbale, full truck trip",2,850000,18,2006000,PO-2026-1235
EM-2026-0229,2026-08-07,Elgon Millers Ltd,Maize flour 25kg bag,739,41000,18,35752820,PO-2026-1242
LL-2026-0449,2026-08-07,Lakeside Logistics Ltd,"Transport Jinja to Soroti, full truck trip",2,1200000,18,2400000,PO-2026-1251
LL-2026-0452,2026-08-08,Lakeside Logistics Ltd,"Transport Jinja to Soroti, full truck trip",2,1200000,18,2832000,PO-2026-1260
BO-2026-0416,2026-08-09,Busoga Oils Ltd,Cooking oil 20L jerrycan,142,82000,18,13739920,PO-2026-1263
EM-2026-0232,2026-08-10,Elgon Millers Ltd,Maize flour 50kg sack,274,80000,18,25865600,PO-2026-1270
BO-2026-0419,2026-08-16,Busoga Oils Ltd,Cooking oil 200L drum,10,730000,18,8614000,PO-2026-1281
BO-2026-0422,2026-08-20,Busoga Oils Ltd,Cooking oil 200L drum,5,730000,18,4307000,
LL-2026-0455,2026-08-21,Lakeside Logistics Ltd,"Transport Jinja to Iganga and Tororo, full truck trip",3,650000,18,2301000,PO-2026-1295
PP-2026-0153,2026-08-21,Pearl Packaging Ltd,"Woven polypropylene bags 25kg, bale of 500",2,275000,18,649000,PO-2026-1303
TR-2026-0093,2026-08-24,Tororo Rice Growers Cooperative,Beans 25kg bag,191,62000,18,13973560,PO-2026-1310
EM-2026-0235,2026-08-25,Elgon Millers Ltd,Maize flour 50kg sack,337,80000,18,31812800,PO-2026-1313
BO-2026-0425,2026-08-26,Busoga Oils Ltd,Cooking oil 200L drum,4,730000,18,3445600,PO-2026-1318
PP-2026-0156,2026-08-26,Pearl Packaging Ltd,"Printed packaging film, roll",1,320000,18,377600,PO-2026-1323
EM-2026-0238,2026-08-29,Elgon Millers Ltd,Maize flour 25kg bag,681,41000,18,32946780,PO-2026-1331
PP-2026-0159,2026-09-01,Pearl Packaging Ltd,"Woven polypropylene bags 25kg, bale of 500",3,275000,18,973050,PO-2026-1342
BO-2026-0428,2026-09-02,Busoga Oils Ltd,Cooking oil 20L jerrycan,200,82000,18,19352000,PO-2026-1346
BO-2026-0431,2026-09-03,Busoga Oils Ltd,Cooking oil 20L jerrycan,288,82000,18,27866880,PO-2026-1356
EM-2026-0241,2026-09-04,Elgon Millers Ltd,Maize flour 25kg bag,387,41000,18,18723060,PO-2026-1366
PP-2026-0162,2026-09-07,Pearl Packaging Ltd,"Printed packaging film, roll",6,320000,18,2265600,PO-2026-1377
BO-2026-0434,2026-09-13,Busoga Oils Ltd,Cooking oil 20L jerrycan,277,82000,18,26802520,PO-2026-1380
BO-2026-0437,2026-09-14,Busoga Oils Ltd,Cooking oil 20L jerrycan,260,82000,18,25157600,PO-2026-1383
EM-2026-0244,2026-09-14,Elgon Millers Ltd,Maize flour 50kg sack,181,80000,18,17086400,PO-2026-1388
BO-2026-0440,2026-09-15,Busoga Oils Ltd,Cooking oil 200L drum,8,730000,18,6891200,PO-2026-1399
TR-2026-0096,2026-09-15,Tororo Rice Growers Cooperative,Beans 25kg bag,149,62000,18,10900840,PO-2026-1403
EM-2026-0247,2026-09-16,Elgon Millers Ltd,Maize flour 50kg sack,276,80000,18,26054400,PO-2026-1410
TR-2026-0099,2026-09-17,Tororo Rice Growers Cooperative,Rice 25kg bag,297,68000,18,23831280,PO-2026-1415
EM-2026-0250,2026-09-20,Elgon Millers Ltd,Maize flour 50kg sack,155,80000,18,14732000,PO-2026-1425
PP-2026-0165,2026-09-20,Pearl Packaging Ltd,"Woven polypropylene bags 25kg, bale of 500",3,275000,18,973500,PO-2026-1435
BO-2026-0443,2026-09-22,Busoga Oils Ltd,Cooking oil 20L jerrycan,179,82000,18,17320040,PO-2026-1445
EM-2026-0253,2026-09-22,Elgon Millers Ltd,Maize flour 25kg bag,495,41000,18,23948100,PO-2026-1454
LL-2026-0458,2026-09-23,Lakeside Logistics Ltd,"Transport Jinja to Mbale, full truck trip",2,850000,18,2006000,PO-2026-1465
BO-2026-0446,2026-09-24,Busoga Oils Ltd,Cooking oil 20L jerrycan,355,82000,18,34349800,PO-2026-1472
LL-2026-0461,2026-09-26,Lakeside Logistics Ltd,"Transport Jinja to Iganga and Tororo, full truck trip",4,650000,18,3068000,PO-2026-1479
TR-2026-0102,2026-09-28,Tororo Rice Growers Cooperative,Beans 25kg bag,112,62000,18,8193920,PO-2026-1488
BO-2026-0449,2026-09-29,Busoga Oils Ltd,Cooking oil 20L jerrycan,192,82000,18,18577920,PO-2026-1497
BO-2026-0452,2026-09-29,Busoga Oils Ltd,Cooking oil 20L jerrycan,151,82000,18,14610760,
LL-2026-0464,2026-10-01,Lakeside Logistics Ltd,"Transport Jinja to Iganga and Tororo, full truck trip",7,650000,0,4550000,PO-2026-1516
PP-2026-0168,2026-10-02,Pearl Packaging Ltd,"Woven polypropylene bags 25kg, bale of 500",4,275000,18,1298000,PO-2026-1527
EM-2026-0256,2026-10-04,Elgon Millers Ltd,Maize flour 25kg bag,766,41000,18,37059080,PO-2026-1536
TR-2026-0093,2026-08-24,Tororo Rice Growers Cooperative,Beans 25kg bag,191,62000,18,13973560,PO-2026-1310
LL-2026-0467,2026-10-04,Lakeside Logistics Ltd,"Transport Jinja to Soroti, full truck trip",5,1200000,18,7080000,PO-2026-1541
LL-2026-0470,2026-10-04,Lakeside Logistics Ltd,"Transport Jinja to Soroti, full truck trip",4,1200000,18,5664000,PO-2026-1544
PP-2026-0171,2026-10-04,Pearl Packaging Ltd,"Cartons for 5L oil, bundle of 100",12,180000,18,2548800,PO-2026-1550
PP-2026-0174,2026-10-04,Pearl Packaging Ltd,"Printed packaging film, roll",1,320000,18,371700,PO-2026-1558
EM-2026-0259,2026-10-05,Elgon Millers Ltd,Maize flour 50kg sack,194,80000,18,18313600,PO-2026-1566
TR-2026-0105,2026-10-07,Tororo Rice Growers Cooperative,Rice 25kg bag,346,68000,18,27763040,PO-2026-1576
TR-2026-0108,2026-10-08,Tororo Rice Growers Cooperative,Rice 25kg bag,359,68000,18,28806160,PO-2026-1585
TR-2026-0111,2026-10-08,Tororo Rice Growers Cooperative,Rice 25kg bag,180,68000,18,14443200,PO-2026-1593
EM-2026-0262,2026-10-10,Elgon Millers Ltd,Maize flour 25kg bag,353,41000,18,17078140,PO-2026-1601
PP-2026-0177,2026-10-10,Pearl Packaging Ltd,"Printed packaging film, roll",3,320000,18,1132800,PO-2026-1605
TR-2026-0114,2026-10-11,Tororo Rice Growers Cooperative,Rice 25kg bag,379,68000,18,30410960,PO-2026-1610
LL-2026-0473,2026-10-13,Lakeside Logistics Ltd,"Transport Jinja to Iganga and Tororo, full truck trip",6,650000,18,4602000,PO-2026-1613
TR-2026-0117,2026-10-14,Tororo Rice Growers Cooperative,Rice 25kg bag,341,68000,18,27361840,PO-2026-1624
LL-2026-0476,2026-10-17,Lakeside Logistics Ltd,"Transport Jinja to Iganga and Tororo, full truck trip",3,650000,18,2301000,PO-2026-1635
TR-2026-0120,2026-10-20,Tororo Rice Growers Cooperative,Rice 25kg bag,135,68000,18,10832400,PO-2026-1638
=== THE REQUEST ENDS ===
Write your answer to: /sessions/focused-youthful-einstein/mnt/IUEA-Teaching-Resources/Professional_AI_Training/Business_AI/Applied AI and Automation - Executive Edition/05 Course Maintenance/Case Runs/runs/F6_invoice_check_RUN.md  (replace RUN with the run number given to you in your task message, for example F6_invoice_check_run1.md).