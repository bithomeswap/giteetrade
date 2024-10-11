import importlib
import traceback
from glob import glob
from pathlib import Path
from types import ModuleType
from typing import Optional, List, Type, Dict

from event import EventEngine, Event
from strategy.object import KlineData, EVENT_KLINE, KlineRequest
from strategy.template import StrategyTemplate
from trader.constant import EVENT_TICK, EVENT_ORDER, EVENT_TRADE, EVENT_POSITION, OrderType, Direction, Exchange, \
    EVENT_CONTRACT, EVENT_LOG, EVENT_ACCOUNT
from trader.engine import BaseEngine, MainEngine
from trader.gateway import BaseGateway
from trader.object import OrderData, TickData, TradeData, PositionData, CancelRequest, SubscribeRequest, OrderRequest, \
    ContractData, LogData, AccountData
from trader.utils import round_to

APP_NAME = "strategy"


class StrategyEngine(BaseEngine):

    def __init__(self, main_engine: MainEngine, event_engine: EventEngine) -> None:
        super(StrategyEngine, self).__init__(main_engine, event_engine, APP_NAME)
        # self.symbol_map = dict()
        self.strategy_templates: Dict[str, Type[StrategyTemplate]] = {}  # 初始化的策略类

        self.strategys: Dict[str, StrategyTemplate] = {}  # 启动的策略
        # self.symbol_strategy_map: Dict[str, Set[StrategyTemplate]] = defaultdict(set)
        # self.orderid_strategy_map: Dict[str, StrategyTemplate] = {}
        # self.add_function()

    # def add_function(self):
    #     self.main_engine.query_stock_kline = self.query_stock_kline

    def init_engine(self) -> None:
        """"""
        self.load_strategy_class()
        # from strategies.hot_leading_strategy import HotLeadingStrategy
        # self.add_strategy_template(HotLeadingStrategy)

        self.register_event()
        self.write_log("策略引擎初始化成功")

    def close(self) -> None:
        """"""
        self.stop_all_strategies()

    def add_strategy_template(self, template: StrategyTemplate) -> None:
        """添加算法类"""
        self.strategy_templates[template.__name__] = template

    def register_event(self) -> None:
        """"""
        self.event_engine.register(EVENT_TICK, self.process_tick_event)
        self.event_engine.register(EVENT_ORDER, self.process_order_event)
        self.event_engine.register(EVENT_TRADE, self.process_trade_event)
        self.event_engine.register(EVENT_POSITION, self.process_position_event)
        self.event_engine.register(EVENT_KLINE, self.process_kline_event)
        self.event_engine.register(EVENT_CONTRACT, self.process_contract_event)
        self.event_engine.register(EVENT_ACCOUNT, self.process_account_event)
        # 概念数据 资金流向 股票信息

    def process_tick_event(self, event: Event) -> None:
        """处理行情事件"""
        tick: TickData = event.data
        for strategy in self.strategys.values():
            strategy.update_tick(tick)

    def process_timer_event(self, event: Event) -> None:
        """处理定时事件"""
        # 生成列表避免字典改变
        algos: List[StrategyTemplate] = list(self.strategys.values())

        for algo in algos:
            algo.update_timer()

    def process_trade_event(self, event: Event) -> None:
        """处理成交事件"""
        trade: TradeData = event.data
        for strategy in self.strategys.values():
            strategy.update_trade(trade)

    def process_order_event(self, event: Event) -> None:
        """处理委托事件"""
        order: OrderData = event.data
        for strategy in self.strategys.values():
            strategy.update_order(order)

    def process_position_event(self, event: Event) -> None:
        """处理持仓事件"""
        position: PositionData = event.data
        for strategy in self.strategys.values():
            strategy.update_position(position)

    def process_account_event(self, event: Event) -> None:
        """处理账户事件"""
        account: AccountData = event.data
        for strategy in self.strategys.values():
            strategy.update_account(account)

    def process_contract_event(self, event: Event) -> None:
        """处理股票信息"""
        contract: ContractData = event.data
        for strategy in self.strategys.values():
            strategy.update_contract(contract)

    def process_kline_event(self, event: Event) -> None:
        """处理历史kline"""
        kline: KlineData = event.data
        for strategy in self.strategys.values():
            strategy.update_kline(kline)

    def _start_strategy(self, template_name: str, setting: dict) -> str:
        # 查询
        if template_name not in self.strategy_templates.keys():
            raise Exception("找不到对应的策略")
        strategy_temp: "StrategyTemplate" = self.strategy_templates[template_name]

        strategy_name: str = f"{strategy_temp.__name__}_"
        # 创建实例
        strategy = strategy_temp(self, strategy_name)

        self.strategys[template_name] = strategy
        # 启动
        strategy.start()
        return template_name

    def start_strategy(self, template_name: str):
        """
        策略类名
        :param template_name:
        :return:
        """
        self._start_strategy(template_name, dict())

    def start_all_strategies(self):
        for k,v in self.strategy_templates.items():
            self._start_strategy(k, dict())

    def stop_all_strategies(self):
        for strategy in self.strategys.values():
            strategy.stop()

    def load_strategy_class(self) -> None:
        """
        Load strategy class from source code.
        """
        # path1: Path = Path(__file__).parent.joinpath("strategies")
        # self.load_strategy_class_from_folder(path1, "strategies")

        path2: Path = Path.cwd().joinpath("strategies")
        # print(path2)
        self.load_strategy_class_from_folder(path2, "strategies")

    def load_strategy_class_from_folder(self, path: Path, module_name: str = "") -> None:
        """
        Load strategy class from certain folder.
        """
        for suffix in ["py", "pyd", "so"]:
            pathname: str = str(path.joinpath(f"*.{suffix}"))
            for filepath in glob(pathname):
                filename = Path(filepath).stem
                name: str = f"{module_name}.{filename}"
                self.load_strategy_class_from_module(name)

    def load_strategy_class_from_module(self, module_name: str) -> None:
        """
        Load strategy class from module file.
        """
        try:
            module: ModuleType = importlib.import_module(module_name)

            # 重载模块，确保如果策略文件中有任何修改，能够立即生效。
            importlib.reload(module)

            for name in dir(module):
                value = getattr(module, name)
                if (isinstance(value, type) and issubclass(value, StrategyTemplate) and value is not StrategyTemplate):
                    self.strategy_templates[value.__name__] = value
        except:  # noqa
            msg: str = f"策略文件{module_name}加载失败，触发异常：\n{traceback.format_exc()}"
            self.write_log(msg)

    def subscribe(self, symbol: str, exchange: Exchange, gateway_name: str) -> None:
        """订阅行情"""
        req: SubscribeRequest = SubscribeRequest(
            symbol=symbol,
            exchange=exchange
        )
        self.main_engine.subscribe(req, gateway_name)

    def send_order(
        self,
        strategy: StrategyTemplate,
        vt_symbol: str,
        direction: Direction,
        price: float,
        volume: float,
        order_type: OrderType,
    ) -> str:
        """委托下单"""
        contract: Optional[ContractData] = self.main_engine.get_contract(vt_symbol)
        volume: float = round_to(volume, contract.min_volume)
        if not volume:
            return ""

        req: OrderRequest = OrderRequest(
            symbol=contract.symbol,
            exchange=contract.exchange,
            direction=direction,
            type=order_type,
            volume=volume,
            price=price,
            reference=f"{APP_NAME}_{strategy.strategy_name}"
        )
        vt_orderid: str = self.main_engine.send_order(req, contract.gateway_name)

        # self.orderid_algo_map[vt_orderid] = strategy
        return vt_orderid

    def cancel_order(self, strategy: StrategyTemplate, vt_orderid: str) -> None:
        """委托撤单"""
        order: Optional[OrderData] = self.main_engine.get_order(vt_orderid)

        if not order:
            self.write_log(f"委托撤单失败，找不到委托：{vt_orderid}", strategy)
            return

        req: CancelRequest = order.create_cancel_request()
        self.main_engine.cancel_order(req, order.gateway_name)

    def get_tick(self, strategy: StrategyTemplate, vt_symbol: str) -> Optional[TickData]:
        """查询行情"""
        tick: Optional[TickData] = self.main_engine.get_tick(vt_symbol)

        if not tick:
            self.write_log(f"查询行情失败，找不到行情：{vt_symbol}", strategy)

        return tick

    def get_position(self, strategy: StrategyTemplate, vt_positionid: str) -> Optional[PositionData]:
        """查询持仓"""
        position: Optional[PositionData] = self.main_engine.get_position(vt_positionid)
        if not position:
            self.write_log(f"查询持仓失败，找不到持仓：{vt_positionid}", strategy)
        return position

    def get_account(self, strategy: StrategyTemplate, vt_accountid: str) -> Optional[AccountData]:
        """查询账户"""
        account: Optional[AccountData] = self.main_engine.get_account(vt_accountid)
        if not account:
            self.write_log(f"查询账户失败，找不到账户：{vt_accountid}", strategy)
        return account

    def get_all_contracts(self) -> List[ContractData]:
        return self.main_engine.get_all_contracts()

    def query_all_contracts(self, gateway_name: str) -> None:
        gateway: BaseGateway = self.main_engine.get_gateway(gateway_name)
        if gateway is not None:
            gateway.query_all_contracts()

    def get_contract(self, strategy: StrategyTemplate, vt_symbol: str) -> Optional[ContractData]:
        """查询合约"""
        contract: Optional[ContractData] = self.main_engine.get_contract(vt_symbol)

        if not contract:
            self.write_log(f"查询合约失败，找不到合约：{vt_symbol}", strategy)

        return contract

    def query_stock_kline(self, gateway_name: str, req: KlineRequest) -> None:
        gateway: BaseGateway = self.main_engine.get_gateway(gateway_name)
        if gateway is not None:
            gateway.query_day_kline(req)

    def query_account(self, gateway_name: str) -> None:
        gateway: BaseGateway = self.main_engine.get_gateway(gateway_name)
        if gateway is not None:
            gateway.query_account()

    def query_position(self, gateway_name: str) -> None:
        gateway: BaseGateway = self.main_engine.get_gateway(gateway_name)
        if gateway is not None:
            gateway.query_position()

    def write_log(self, msg: str, strategy: StrategyTemplate = None) -> None:
        """
        记录日志
        """
        if strategy:
            msg: str = f"[{strategy.strategy_name}]  {msg}"

        log: LogData = LogData(msg=msg, gateway_name=APP_NAME)
        event: Event = Event(type=EVENT_LOG, data=log)
        self.event_engine.put(event)
        # print(f"StrategyEngine:{msg}")


class ValueAddEngine(BaseEngine):

    def __init__(self, main_engine: MainEngine, event_engine: EventEngine) -> None:
        super().__init__(main_engine, event_engine, "value")
        self.add_function()
        self.register_event()

    def add_function(self):

        self.main_engine.query_stock_kline = self.query_stock_kline

    def register_event(self):
        self.event_engine.register(EVENT_KLINE, self.process_kline_event)

    def query_stock_kline(self):
        pass

    def process_kline_event(self, event: Event) -> None:
        pass


if __name__ == '__main__':
    # from hot_leading_strategy import HotLeadingStrategy
    # print(HotLeadingStrategy.__name__)

    engine = StrategyEngine(None,None)
    engine.init_engine()
    pass
