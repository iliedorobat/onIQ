from ro.webdata.oniq.validation.dataset.direct_questions.aux_pairs import DID_PAIRS, DO_PAIRS
from ro.webdata.oniq.validation.dataset.direct_questions.who_pairs import WHO_PAIRS
from ro.webdata.oniq.validation.dataset.direct_questions.whom_pairs import WHOM_PAIRS
from ro.webdata.oniq.validation.dataset.direct_questions.whose_pairs import WHOSE_PAIRS
from ro.webdata.oniq.validation.dataset.what.what_pairs import WHAT_PAIRS
from ro.webdata.oniq.validation.dataset.what.what_do_pairs import WHAT_DO_PAIRS
from ro.webdata.oniq.validation.dataset.what.what_is_pairs import WHAT_IS_PAIRS
from ro.webdata.oniq.validation.dataset.which.which_pairs import WHICH_PAIRS
from ro.webdata.oniq.validation.dataset.which.which_is_pairs import WHICH_IS_PAIRS
from ro.webdata.oniq.validation.dataset.measurable_questions.how_pairs import HOW_PAIRS, HOW_IS_PAIRS
from ro.webdata.oniq.validation.dataset.where.where_pairs import WHERE_PAIRS
from ro.webdata.oniq.validation.dataset.where.where_do_pairs import WHERE_DO_PAIRS
from ro.webdata.oniq.validation.dataset.where.where_is_pairs import WHERE_IS_PAIRS
from ro.webdata.oniq.validation.dataset.when.when_pairs import WHEN_PAIRS
from ro.webdata.oniq.validation.dataset.when.when_do_pairs import WHEN_DO_PAIRS
from ro.webdata.oniq.validation.dataset.when.when_is_pairs import WHEN_IS_PAIRS
from ro.webdata.oniq.validation.dataset.why.why_pairs import WHY_PAIRS

PAIRS = DO_PAIRS + DID_PAIRS + \
        HOW_PAIRS + HOW_IS_PAIRS + \
        WHAT_PAIRS + WHAT_DO_PAIRS + WHAT_IS_PAIRS + \
        WHEN_PAIRS + WHEN_DO_PAIRS + WHEN_IS_PAIRS + \
        WHERE_PAIRS + WHERE_DO_PAIRS + WHERE_IS_PAIRS + \
        WHICH_PAIRS + WHICH_IS_PAIRS + \
        WHO_PAIRS + WHOM_PAIRS + WHOSE_PAIRS + \
        WHY_PAIRS

# [1] https://raw.githubusercontent.com/smart-task/smart-dataset/master/datasets/DBpedia/smarttask_dbpedia_train.json
#   * ISWC 2020 SMART challenge: https://smart-task.github.io/
# [2] https://sci-hub.tw/10.1007/978-3-540-72667-8_34 (PANTO pp. 6)
# [3] https://github.com/LiberAI/NSpM/blob/master/data/monument_300.zip
# [4] https://github.com/SmartDataAnalytics/ARCANA/blob/master/ARCANA%20Questions/Test_Data_Set/TestNow.txt
# [5] https://github.com/BaiBlanc/neural-qa/blob/master/data/monument_300.zip
# [6] https://www.englishclub.com/vocabulary/wh-question-words.htm
