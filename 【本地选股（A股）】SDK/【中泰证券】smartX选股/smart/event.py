
# smart提供的事件定义
class Event():
    ON_INIT = "on_init"
    ON_SHOW = "on_show"  # todo：绍光
    ON_HIDE = "on_hide"  # todo：绍光
    ON_CLOSE = "on_close"  # todo：绍光
    ON_RESET = "on_reset"  # todo：绍光  作用？？？？？
    ON_QUOTE = "on_quote"  # 账户订阅行情后，行情变化推送
    ON_BAR = "on_bar" # 账户订阅指标行情后，bar、macd行情变化推送
    ON_INDICATOR = "on_indicator" # 账户订阅通用指标行情后，行情变化推送
    ON_STRATEGY_QUOTE = "on_strategy_quote"  # 某策略订阅的行情推送 策略之间、组件之间、策略和账户直接的订阅和取消订阅不相互影响
    ON_ORDER = "on_order"  # 委托变化推送
    # ON_STRATEGY_ORDER = "on_strategy_order"  # 某策略的委托变化推送  #todo：魏义
    ON_TRADE = "on_trade"  # 成交变化推送
    # ON_STRATEGY_TRADE = "on_strategy_trade"  # 某策略的委托变化推送  #todo：魏义
    ON_CANCEL_FAIL = "on_cancel_fail"  # 撤单失败的消息推送
    ON_POSITION = "on_position"  # 账户持仓变化的增量推送
    ON_POSITION_REFRESH_ALL = "on_position_refresh_all"  # 账户持仓变化的全量推送
    # ON_STRATEGY_POSITION = "on_strategy_position"  # 某策略持仓变化的增量推送  #todo：魏义
    # ON_STRATEGY_POSITION_REFRESH_ALL = "on_strategy_position_refresh_all"  # 某策略持仓变化的全量推送 #todo：魏义
    ON_ASSETS = "on_assets"  # 账户资金的全量推送
    ON_BOOK = "on_book"  # 某策略账簿的全量推送 #todo：魏义
    ON_STRATEGY_CANCEL_FAIL = "on_strategy_cancel_fail"  # 某策略撤单失败消息推送 #todo:魏义
    ON_STRATEGY_UPLOAD_RESULT = "on_strategy_upload_result"  # 某策略上传结果事件 isFrontStrategy为true的前台策略无需上传 #todo：魏义
    # ON_STRATEGY_START_RESULT = "on_strategy_start_result"  # 某策略启动结果消息 #todo：魏义
    # ON_STRATEGY_STOP_RESULT = "on_strategy_stop_result"  # 某策略停止结果消息  #todo：魏义
    ON_STRATEGY_FORCE_STOP_RESULT = "on_strategy_force_stop_result"  # 某策略强制停止结果消息 #todo：魏义
    ON_STRATEGY_EXCEPTION = "on_strategy_exception"  # 某策略运行中的异常消息  如td md断线  程序异常等等  不论前后台策略 抛出的异常都可以 回调有个入参区分前台还是后台 #todo：魏义
    ON_STRATEGY_LOG = "on_strategy_log"  # 某策略log日志发生变化时的增量变化消息 后端策略时取后台日志 前台策略时：取前台console日志 #todo：魏义
    ON_STRATEGY_PRE_START = "on_strategy_pre_start"  # 后端策略时：后台策略pre_start后触发 或 前台策略时：前台策略start后触发 #todo：魏义
    ON_STRATEGY_POST_START = "on_strategy_post_start"  # 后端策略时：后台策略post_start后 或 后端策略时：前台策略pre_start后触发 #todo：魏义
    ON_STRATEGY_PRE_STOP = "on_strategy_pre_stop"  # 后端策略时：后台策略pre_stop后或 后端策略时：前台策略stop前触发 #todo：魏义
    ON_STRATEGY_STATUS_CHANGE = "on_strategy_status_change"  # 策略状态变化时推送
    ON_ALPHAX_TD_STATUS_CHANGE = "on_alphax_td_status_change"  # alphax td状态变化时推送
    ON_ALPHAX_MD_STATUS_CHANGE = "on_alphax_md_status_change"  # alphax md状态变化时推送
    ON_ALPHAX_MSG = "on_alphax_msg"  # alphax 策略往前端推送数据
    ON_ETF_PROFIT = "on_etf_profit"  # ETF 折溢价利润推送数据
    ON_ETF_RATE_UPDATE = "on_etf_rate_update"  # 更新ETF套利/交易费用设置通知
    ON_SYSTEM_SET_UPDATE = "on_system_set_update"  # 更新系统全局常用设置项通知
    ON_CREDIT_TICKER_ASSIGN ="on_credit_ticker_assign" #更新信用账户可融券头寸信息
    ON_CREDIT_DEBT_FINANCE = "on_credit_debt_finance" #更新融资负债合约信息
    ON_CREDIT_DEBT_SECURITY = "on_credit_debt_security" #更新融券负债合约信息

    UPDATE_ENTRUST = "UPDATE_ENTRUST"
    UPDATE_TRADE_REPORT = "UPDATE_TRADE_REPORT"
    CANCEL_ORDER_FAIL_RSP = "CANCEL_ORDER_FAIL_RSP"
    CANCEL_ORDER_SUCC_RSP = "CANCEL_ORDER_SUCC_RSP"
    UPDATE_ASSETS = "UPDATE_ASSETS"
    UPDATE_POSITION = "UPDATE_POSITION"
    REFRESH_POSITION = "REFRESH_POSITION"
    QUOTE = "QUOTE"
    QUOTEBAR = "QUOTEBAR"
    QUOTEINDICATOR = "QUOTEINDICATOR"
    ETF_RATE_UPDATE = "ETF_RATE_UPDATE"
    SYSTEM_SET_UPDATE = "SYSTEM_SET_UPDATE"
    UPDATE_ETF_PROFIT = "UPDATE_ETF_PROFIT"
    INIT_ALL_TICKERS = "INIT_ALL_TICKERS"
    UPDATE_CREDIT_ASSETS = "UPDATE_CREDIT_ASSETS"
    UPDATE_CREDIT_TICKER_ASSIGN_INFO = "UPDATE_CREDIT_TICKER_ASSIGN_INFO"
    UPDATE_CREDITDEBTINFO_CASH = "UPDATE_CREDITDEBTINFO_CASH"
    UPDATE_CREDITDEBTINFO_SECURITY = "UPDATE_CREDITDEBTINFO_SECURITY"
    INIT_DATA_TYPE = "INIT_DATA_TYPE"