import time

class Timer():
  on_finish = None
  on_count = None
  def __init__(self, default_countdown: int, in_console: bool = True):
    self.set_default_countdown(default_countdown)
    self.in_console = in_console
    self.__is_playing = False
    self.finished = False

  def start(self):
    self.__is_playing = True
    self.__countdown_start = self.actual_count
    self.play()

  def play(self):
    self.__is_playing = True
    for i in range(self.__countdown_start, -1, -1):
      self.actual_count = i

      if self.on_count:
        self.on_count()

      if not self.__is_playing:
        break
      else:
        if self.in_console:
          print(self.actual_count)

      time.sleep(1)

    self.finished = True
    if self.on_finish:
      self.on_finish()

  def pause(self):
    self.__is_playing = False
    self.finished = False

  def reset(self):
    self.actual_count = self.__default_countdown
    self.finished = False

  def stop(self):
    self.actual_count = self.__default_countdown
    self.finished = True

  def set_default_countdown(self, default_countdown: int):
    self.__default_countdown = default_countdown
    self.__countdown_start = default_countdown
    self.actual_count = default_countdown

  def get_default_countdown(self):
    return self.__default_countdown

  def set_start_countdown(self, start_countdown: int):
    self.__countdown_start = start_countdown

  def get_start_countdown(self):
    return self.__countdown_start
