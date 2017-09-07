# Epsilon-heatmap

This simple program is able to take the typical PDF report created by the proprietary Epsilon software which can report stress echocardiography.

![alt text](http://jamesphoward.com/ehm-report.PNG)

It performs two processes

1) It reformats the data to the traditional 17 segment model often used in research, rather than the 18 segment model provided

2) It extracts the pixel colours from the 17 segments, allowing quantitative analysis, for example:

```
segment	red	redpink	pink	white	lightblue	blue	darkblue
1	0	632	1297	603	0	0	0
2	18	2280	18	0	0	0	0
3	0	1281	856	0	0	0	0
4	0	778	1283	485	0	0	0
5	19	2263	0	0	0	0	0
6	0	1129	928	0	0	0	0
7	1064	761	0	0	0	0	0
8	0	1368	210	0	0	0	0
9	1064	341	0	0	0	0	0
10	1052	651	0	0	0	0	0
11	0	1318	222	0	0	0	0
12	1039	425	0	0	0	0	0
13	415	626	345	236	53	0	0
14	666	293	634	67	0	0	0
15	399	656	355	255	39	0	0
16	649	307	564	32	0	0	0
17	95	309	319	259	250	607	0
```
