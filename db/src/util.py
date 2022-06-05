import typing as T

class DotDict(T.Dict[str, T.Any]):
  """Allows dot notation for access to dictionary attributes

  Both get and set attributes are available

  Examples:
      ::

          dd = DotDict({'a': 1, 'b':2})
          dd.a + dd.b # 3

          dd2 = DotDict(msg1 = 'hello', msg2 = 'world')
          print(f'{dd2.msg1} {dd2.msg2}') # hello world

          dd3 = DotDict(longer_name = spark.createDataFrame(pd.DataFrame({'a': [1,2]})))
          dd3.alias('longer_name', 'short_name')
          dd3.short_name
  """

  def __getattr__(self, *args: T.Any):
    val = self.get(*args)
    return DotDict(val) if type(val) is dict else val

  def __setattr__(self, key: str, val: T.Any) -> None:
    return self.__setitem__(key, val)

  def __delattr__(self, key):
    return self.__delitem__(key)

  def alias(self, tname, newname):
    self[newname] = self[tname]
    return self
