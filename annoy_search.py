from annoy import AnnoyIndex
import logging
import logging.config


logging.config.fileConfig(fname='log.config', disable_existing_loggers=False)


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


# 使用annoy进行相似(最近邻)搜索
@ singleton
class AnnoySearch:

    def __init__(self, vec_dim=100, metric='angular'):
        self.vec_dim = vec_dim  # 要index的向量维度
        self.metric = metric    # 度量可以是"angular"，"euclidean"，"manhattan"，"hamming"，或"dot"
        self.annoy_instance = AnnoyIndex(self.vec_dim, self.metric)
        self.logger = logging.getLogger('AnnoySearch')

    def save_annoy(self, annoy_file, prefault=False):
        self.annoy_instance.save(annoy_file, prefault=prefault)
        self.logger.info('save annoy SUCCESS !')

    def unload_annoy(self):
        self.annoy_instance.unload()

    def load_annoy(self, annoy_file, prefault=False):
        try:
            self.annoy_instance.unload()
            self.annoy_instance.load(annoy_file, prefault=prefault)
            self.logger.info('load annoy SUCCESS !')
        except FileNotFoundError:
            self.logger.error(
                'annoy file DOES NOT EXIST , load annoy FAILURE !',
                exc_info=True)

    # 创建annoy索引
    def build_annoy(self, n_trees):
        self.annoy_instance.build(n_trees)

    # 查询最近邻，通过index
    def get_nns_by_item(
            self,
            index,
            nn_num,
            search_k=-1,
            include_distances=False):
        return self.annoy_instance.get_nns_by_item(
            index, nn_num, search_k, include_distances)

    # 查询最近邻，通过向量
    def get_nns_by_vector(
            self,
            vec,
            nn_num,
            search_k=-1,
            include_distances=False):
        return self.annoy_instance.get_nns_by_vector(
            vec, nn_num, search_k, include_distances)

    def get_n_items(self):
        return self.annoy_instance.get_n_items()

    def get_n_trees(self):
        return self.annoy_instance.get_n_trees()

    def get_vec_dim(self):
        return self.vec_dim

    # 添加item
    def add_item(self, index, vec):
        self.annoy_instance.add_item(index, vec)

    def get_item_vector(self, index):
        return self.annoy_instance.get_item_vector(index)


if __name__ == '__main__':

    import random

    ann_s = AnnoySearch(10)
    for i in range(100):
        v = [random.gauss(0, 1) for z in range(10)]
        ann_s.add_item(i, v)
    ann_s.build_annoy(10)
    ann_s.save_annoy('test.annoy')

    ann_s.load_annoy('test.annoy')
    res = ann_s.get_nns_by_vector([random.gauss(0, 1) for z in range(10)], 2)
    print(res)
    # print(ann_s.get_item_vector(res[0]))
    print(ann_s.get_n_items())
    print(ann_s.get_vec_dim())
