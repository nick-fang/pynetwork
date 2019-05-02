"""实现Order类，支持插入式折扣策略，使用一等函数重构"""
from abc import ABC, abstractmethod
from collections import namedtuple

Customer=namedtuple('Customer', 'name fidelity') #代表一个顾客，由帐户名和会员积分组成

class LineItem: #代表单种商品
    def __init__(self, product, quantity, price): #商品名、单种商品数量、单价
        self.product=product
        self.quantity=quantity
        self.price=price

    def total(self): #单种商品的总价
        return self.price * self.quantity

class Order: #上下文
    def __init__(self, customer, cart, promotion=None): #顾客、购物车、最终可享受的折扣
        self.customer=customer
        self.cart=cart
        self.promotion=promotion

    def total(self): #享受折扣前，购物车中所有商品的总价
        if not hasattr(self, '__total'):
            self.__total=sum(item.total() for item in self.cart) #对购物车中每种商品的总价进行求和
        return self.__total

    def due(self): #最终应付款
        if self.promotion is None:
            discount=0
        else:
            discount=self.promotion(self) #计算折扣值
        return self.total()-discount

    def __repr__(self):
        fmt='<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())

promos=[]
def promotion_reg(promo_func):
    """注册折扣函数的装饰器"""
    promos.append(promo_func)
    return promo_func

@promotion_reg
def fidelity(order):
    """为积分为1000或以上的顾客提供5%折扣"""
    return order.total()*0.05 if order.customer.fidelity >= 1000 else 0

@promotion_reg
def bulk_item(order):
    """单个商品为20个或以上时提供10%折扣"""
    discount=0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total()*0.1 #该单种商品可享受的折扣值
    return discount

@promotion_reg
def large_order(order):
    """订单中的不同商品达到10个或以上时提供7%折扣"""
    distinct_items={item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total()*0.07
    return 0

def best_promo(order):
    """选择可用的最佳折扣"""
    return max(promo(order) for promo in promos)

joe=Customer('john doe', 0)
ann=Customer('ann smith', 1100)
cart=[LineItem('banana', 4, 0.5), 
      LineItem('apple', 10, 1.5), 
      LineItem('watermelon', 5, 5.0)]
banana_cart=[LineItem('banana', 30, 0.5), 
             LineItem('apple', 10, 1.5)]
long_order_cart=[LineItem(str(item_code), 1, 1.0) for item_code in range(10)] #这是个列表推导式
#Order(joe, cart, fidelity_promo)
#Order(ann, cart, fidelity_promo)
#Order(joe, banana_cart, bulk_item_promo)
#Order(joe, long_order_cart, large_order_promo)
#Order(joe, cart, large_order_promo)

Order(joe, long_order_cart, best_promo)
Order(joe, banana_cart, best_promo)
Order(ann, cart, best_promo)