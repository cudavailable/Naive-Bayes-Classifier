**数据：**搜狗文本分类语料库  

**分类器：**朴素贝叶斯分类器 NBC(Naive Bayesian Classifier)   

**编程语言：**Python+jieba分词库+nltk+sklearn  

**改进：**  
	
	1. 应该在处理每个文本的时候，应该去除一些杂乱信息，减少内存占用等  
	2. 如果在事先有词典的情况下，可以直接提取文本特征  
	3. 没有词典的时候，应该自己构造词典，甚至在大量样本中学习词典。由于没有事先的词典dict，把所有文档的分词结果放到一个dictionary里面，然后根据词频从高到低排序。由于处理每个文档的时候，就没有去除一些杂乱信息，比如标点符号、无意义的数字等，所以在试验中构造最终词典(固定选取1000个词)的时候，逐渐去除词典的部分高频项，观察正确率的变化  
	4. 特征维数的选取，在本文中固定1000维，可以做正确率关于维数的变化    
	5. 特别说明：因为分类器用的是朴素贝叶斯，所以文本特征是[TRUE, FALSE, ...]。文本是否包含字典中词的判别p(feature_i | C_k) = ...如果是使用SVM，那么特征应该是词频或者TDIDF等  
	6. 可以采用nltk或sklearn，注意其中选取的特征格式不同。nltk要求特征为dict格式，sklearn要求特征为list  
    
---
以上为原作者@lining0806所述  


## 文件说明
- NBC.py : 数据预处理、朴素贝叶斯分类器的训练和测试
- verify.py : 将爬取的新闻文档作为验证数据集进行验证
- crawl.py : 网络爬虫爬取文档并保存到本地路径
- logger.py : 包含一个日志类，声明之后可以将输出到控制台的内容保存到本地日志中
- requirements.txt : conda环境配置
- stopwords_cn.txt : 不会选做特征词的分词
- result.png : 不同deleteN下的测试准确率

## 文件夹说明
- Database : 训练&测试数据集
- best_model : 存放最佳模型的参数
- log : 包含训练测试日志(log.txt)、最佳模型选取的特征词(feature_words.txt)、验证数据集分类结果(predict.csv)
- news : 爬取之后保存到本地的新闻文档，作为验证数据集

## 我的添加
1. 测试过程中根据测试准确率保存最佳模型的参数，并将输出到控制台的内容保存到本地日志中
2. 通过网络爬虫爬取的新闻文档验证保存的模型的分类准确度

## 改进方向
**问题：**   
	模型的验证准确度低  
   
**可能的原因：**  
	1.特征维数较低；  
 	2.选取的词不具有代表性；  
  	3.作者收集的数据集(Database)来自于9年前的新闻，当时的用词可能和现在的新闻用词有差别；  
   	4.朴素贝叶斯分类器的分类能力有限。  
