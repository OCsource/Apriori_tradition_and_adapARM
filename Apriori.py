from numpy import *

# 全局变量，决定用AdapARM算法还是传统算法
ISARM = 0

# 获取候选项集C1
# 参数：originalData为原始事务集
# 返回list（每个元素都是set集合）
def createC1(originalData):
    C1 = []
    for items in originalData:
        for item in items:
            if not [item] in C1:
                C1.append([item])
    C1.sort()   # 排序，为了消除相同数据而位置不同的情况
    return list(map(frozenset, C1))

# 获取候选集中的频繁项集
# 参数：originalData为原始事务集，Ck（C1,C2...），minSupport最小支持度
# retList为Ck的频繁项集（list），supportData返回频繁项集的支持度（dic）
def findL(originalData, Ck, minSupport):
    candidateCount = {}
    for oneData in originalData:
        for candidate in Ck:
            if candidate.issubset(oneData):
                candidateCount[candidate] = candidateCount.get(candidate, 0) + 1
    numItems = float(len(originalData))
    retList = []
    supportData = {}

    if ISARM == 0:
        # 传统算法
        for k in candidateCount:
            support = candidateCount[k] / numItems
            if support >= minSupport:
                retList.insert(0 , k)
                supportData[k] = support
    else:
        # AdapARM算法(最小支持度为一个大于一的数，求候选集个数大于这个最小支持度的数)
        for k in candidateCount:
            support = candidateCount[k] / numItems
            if candidateCount[k] >= minSupport:
                retList.insert(0 , k)
                supportData[k] = support

    return retList, supportData

# 生成下一个候选项集C(k+1)
# 参数：Lk频繁项集,项集数k
# 返回候选项集C(k+1)（list）
def getNextCandidate(Lk, k):
    retList = []
    for i in range(len(Lk)):
        for j in range(i + 1, len(Lk)):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1 == L2:    # 两个集合有k-1项相同，进行合并
                retList.append(Lk[i] | Lk[j])
    return retList

# 获取所有的频繁项集
# 参数：originalData为原始事务集，minSupport最小支持度，isARM决定是否用AdapARM算法
# 返回C候选项集(list)，L频繁项集（list），supportData返回频繁项集的支持度（dic）
def apriori(originalData, minSupport, isARM):
    global ISARM
    ISARM = isARM
    C1 = createC1(originalData)
    S = list(map(set, originalData))
    L1, supportData = findL(S, C1, minSupport)
    C = [C1]
    L = [L1]
    k = 2
    while(len(L[k-2]) > 0):
        Ck = getNextCandidate(L[k-2], k)
        Lk, supK = findL(S, Ck, minSupport)
        C.append(Ck)
        L.append(Lk)
        supportData.update(supK)
        k += 1
    return C, L, supportData


# 用于自适应关联规则
# 获取大于最小置信度的关联规则
# 参数：supportData频繁项集的支持度，minConfidence最小置信度
# 返回符合条件的列表（list）
def associationRules(supportData, minConfidence):
    elementList = []
    elementDic = {}
    for element in supportData:
        if supportData[element] >= minConfidence and len(element) > 1:
            elementList.append(element)
            elementDic[",".join(list(element))] = supportData[element]
    return elementList, elementDic


# 用于计算关联规则
# 关联结果的右侧只有一条数据
# 参数：Lkn频繁项集里的元素，H Lkn项集中所有的元素，rule规则(元组)，minConfidence最小置信度，supportData频繁项集的支持度
# 返回右侧的元素(list)
def ruleSingle(Lkn, H, rule, minConfidence, supportData):
    rightElements = []
    for element in H:
        conf = supportData[Lkn] / supportData[Lkn-element]
        if conf >= minConfidence:
            # resultDic[",".join(list(Lkn - element)) + "=>" ",".join(list(element))] = conf
            rule.append((Lkn - element, element, conf))
            rightElements.append(element)
    return rightElements

# 关联规则的右侧有多条数据
# 参数：Lkn频繁项集里的元素，H Lkn项集中所有的元素，rule规则，minConfidence最小置信度，supportData频繁项集的支持度
# 无返回值(递归调用)
def rulesFromRight(Lkn, H, rule, minConfidence, supportData):
    if len(Lkn) > len(H[0]) + 1:
        tempC = getNextCandidate(H, len(H[0]) + 1)
        tempH = ruleSingle(Lkn, tempC, rule, minConfidence, supportData)
        # 元素大于一递归
        if len(tempH) > 1:
            rulesFromRight(Lkn, tempH, rule, minConfidence, supportData)

# 用于调用getRule与rulesFromRight生成关联规则
# 参数：L频繁项集，minConfidence最小置信度，supportData频繁项集的支持度
# 返回规则（list）
def getRule(L, minConfidence, supportData):
    rule = []
    for i in range(1, len(L)):
        for Lkn in L[i]:
            # H = list(map(frozenset, Lkn))
            H = [frozenset([item]) for item in Lkn]
            if i > 1:
                rulesFromRight(Lkn, H, rule, minConfidence, supportData)
            else:
                ruleSingle(Lkn, H, rule, minConfidence, supportData)
    return rule
