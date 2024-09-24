from tools.entities import Alias, TestEntity

a =  Alias(alias='aaa', name='bbb')

t = TestEntity(fullname='Test')
t.set_display_info(content=None, title=None)
t.set_note(note=None)
t.set_icon(url=None)
hash(a)
pass