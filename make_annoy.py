from annoy_search import AnnoySearch
import logging
import logging.config


logging.config.fileConfig(fname='log.config', disable_existing_loggers=False)


def make_annoy(vec_dim, vec_list):
    logger = logging.getLogger('make_annoy')
    ann_s = AnnoySearch(vec_dim)
    for i in range(len(vec_list)):
        try:
            ann_s.add_item(i, vec_list[i])
        except IndexError:
            logger.error(
                'dim of vector DOES NOT match with annoy, line ' + str(i + 1),
                exc_info=False)
    logger.info('make annoy SUCCESS !')


if __name__ == '__main__':
    
    vec = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    make_annoy(4, vec)
