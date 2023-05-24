from PyPDF2 import PdfReader

reader = PdfReader("/home/luman/文档/01-数据结构与算法之美/02-入门篇 (4讲)/03丨复杂度分析（上）：如何分析、统计算法的执行效率和资源消耗？.pdf")
for i in range(len(reader.pages)):
    page = reader.pages[i]
    print(page.extract_text())
    print()