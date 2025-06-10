from wxcloudrun.model import db, Counter

# 示例：获取计数器

def get_counter():
    return Counter.query.first()

# 示例：更新计数器

def update_counter(value):
    counter = Counter.query.first()
    if not counter:
        counter = Counter(count=value)
        db.session.add(counter)
    else:
        counter.count = value
    db.session.commit()
    return counter 