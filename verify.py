"""
作用：
	在NBC.py 的 main函数执行完之后做验证

步骤：
	1.使用jieba切分预先爬取的新闻文档，准备verify_data_list（类似于NBC.TextProcessing）
	2.将训练时保存在日志文件夹里的特征词加载出来(feature_words)
	3.根据特征词，构造文档对应的特征向量（类似于NBC.TextFeatures）
	4.加载已经保存下的训练好的分类器模型，将特征向量输入模型，得到预测标签
"""
import re
import jieba
import joblib


def TextProcessing(file_path):
	verify_data_list = []

	with open(file_path, "r", encoding='utf-8') as fp:
		raw = fp.read()

	word_cut = jieba.cut(raw, cut_all=False) # 精确模式
	word_list = list(word_cut) # 转化成list

	verify_data_list.append(word_list)

	return verify_data_list

def get_feature_words(feature_path):
	with open(feature_path, 'r', encoding='utf-8') as fp:
		feature_words = [line.strip() for line in fp]
		return feature_words

def TextFeatures(verify_data_list, feature_words, flag='nltk'):
	def text_features(text, feature_words):
		text_words = set(text)
		if flag == 'nltk':
			features = {word:1 if word in text_words else 0 for word in feature_words}
		elif flag == 'sklearn':
			features = [1 if word in text_words else 0 for word in feature_words]
		else:
			features = []

		return features

	verify_feature_list = [text_features(text, feature_words) for text in verify_data_list]
	return verify_feature_list

def get_class_dict(class_path):
	# 获取类编号和类名对应的字典
	class_dict = {}
	pattern = re.compile(r"(\S+)\s+(\S+)")
	with open(class_path, 'r', encoding='utf-8') as fp:
		for line in fp.readlines():
			match = pattern.match(line.strip())
			if match:
				code, category = match.groups()
				class_dict[code] = category  # 将编号作为键，类名作为值存入字典

	return class_dict

if __name__ == '__main__':

	# 获取类编号与类名对应的字典
	class_path = './Database/SogouC/ClassList.txt'
	class_dict = get_class_dict(class_path)

	# 获取验证文档数据
	verify_data_path = './news/“一个西方关键盟友要倒向俄罗斯”.txt'
	verify_data_list = TextProcessing(verify_data_path)

	# 关键词应该是训练时就确定了的，所以应该在训练时保存feature_words
	feature_path = './log/feature_words.txt'
	feature_words = get_feature_words(feature_path)

	# 根据特征词，构造文档对应的特征向量
	verify_feature_list = TextFeatures(verify_data_list, feature_words, flag='sklearn')

	# 加载已经保存下的训练好的分类器模型，将特征向量输入模型，得到预测标签
	model_path = './best_model/multinomial_nb_model.joblib'
	classifier = joblib.load(model_path)
	labels = classifier.predict(verify_feature_list)
	print(f"{labels[0]} {class_dict[labels[0]]}")