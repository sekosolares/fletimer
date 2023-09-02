from utils.timer import Timer
import flet as ft
import re

def contains_non_numbers(string):
  pattern = r'\D'  # \D matches any non-digit character
  match = re.search(pattern, string)
  return match is not None

def extract_numbers(string):
  numbers = re.findall(r'\d+', string)  # \d+ matches one or more digits
  return numbers

def main(page: ft.Page):
  # Sound Effect by https://pixabay.com/es/users/microsammy-22905943/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=8761">Microsammy</a> from <a href="https://pixabay.com/sound-effects//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=8761
  ALARM_AUDIO_SRC = 'clock-alarm.mp3'

  def set_countdown_field_disabled(e, disabled):
    countdown_field.disabled = disabled
    page.update()

  def update_text_count(e, text: str):
    if text == '0':
      text_to_show.value = 'Times Up!'
      play_alarm(e)
    else:
      text_to_show.value = text
    page.update()

  def set_text_count(e, text: str):
    text_to_show.value = text
    page.update()

  def on_time_change(e):
    if contains_non_numbers(countdown_field.value):
      countdown_field.value = extract_numbers(countdown_field.value)[0]
      set_text_count(e, countdown_field.value)
      page.update()
      return
    if countdown_field.value != '':
      timer.set_default_countdown(int(countdown_field.value))
      set_text_count(e, countdown_field.value)
    else:
      timer.set_default_countdown(0)
      set_text_count(e, '0')

  def play_alarm(e):
    alarm_audio.pause()
    alarm_audio.volume = 1
    alarm_audio.autoplay = False
    alarm_audio.play()
    page.update()

  def stop_countdown(e):
    alarm_audio.pause()
    actions_row.controls = [
      countdown_field_container,
      start_button_container
    ]
    page.update()

    set_countdown_field_disabled(e, False)
    start_button.on_click = start_countdown

    timer.stop()
    actual_countdown = timer.actual_count
    text_to_show.value = f"{actual_countdown}"
    page.update()

  def start_countdown(e):
    alarm_audio.pause()
    page.update()
    actions_row.controls = [
      countdown_field_container,
      stop_button_container,
      pause_button_container
    ]
    set_countdown_field_disabled(e, True)
    on_time_change(e)

    timer.on_count = lambda: update_text_count(e, f'{timer.actual_count}')
    timer.on_finish = lambda: set_countdown_field_disabled(e, False)
    timer.start()
    update_text_count(e, f'{timer.actual_count}')
    page.update()

  def pause_countdown(e):
    actions_row.controls = [
      countdown_field_container,
      stop_button_container,
      start_button_container
    ]
    start_button.on_click = resume_countdown
    set_countdown_field_disabled(e, True)
    update_text_count(e, f'{timer.actual_count}')
    timer.pause()
    page.update()

  def resume_countdown(e):
    actions_row.controls = [
      countdown_field_container,
      stop_button_container,
      pause_button_container
    ]
    page.update()

    set_countdown_field_disabled(e, True)
    timer.on_count = lambda: update_text_count(e, f'{timer.actual_count}')
    timer.on_finish = lambda: set_countdown_field_disabled(e, False)
    timer.play()
    update_text_count(e, f'{timer.actual_count}')
    page.update()

  page.title = "Fletimer"
  page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
  page.vertical_alignment = ft.MainAxisAlignment.CENTER

  title = ft.Text("Fletimer", size=40, weight=ft.FontWeight.BOLD)

  countdown_field = ft.TextField(label="Seconds", value="0", keyboard_type=ft.KeyboardType.NUMBER)
  countdown_field.on_change = on_time_change
  countdown_field.text_align = "center"

  text_to_show = ft.Text("0", size=40, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE)

  timer = Timer(int(countdown_field.value), in_console=False)

  alarm_audio = ft.Audio(
    src=ALARM_AUDIO_SRC,
    balance=0,
    volume=0,
    autoplay=True
  )

  start_button = ft.ElevatedButton(
    text="Start",
    on_click=start_countdown,
    bgcolor=ft.colors.GREEN,
    icon=ft.icons.PLAY_ARROW
  )
  start_button.color = ft.colors.BLACK

  stop_button = ft.ElevatedButton(
    icon=ft.icons.STOP,
    bgcolor=ft.colors.RED,
    on_click=stop_countdown,
    text="Stop"
  )
  stop_button.color = ft.colors.BLACK

  pause_button = ft.ElevatedButton(
    icon=ft.icons.PAUSE,
    bgcolor=ft.colors.YELLOW,
    on_click=pause_countdown,
    text="Pause"
  )
  pause_button.color = ft.colors.BLACK


  countdown_field_container = ft.Container(width=100)
  countdown_field_container.content = countdown_field

  start_button_container = ft.Container(width=150)
  start_button_container.content = start_button

  stop_button_container = ft.Container(width=150)
  stop_button_container.content = stop_button

  pause_button_container = ft.Container(width=150)
  pause_button_container.content = pause_button

  actions_row = ft.Row([countdown_field_container, start_button_container])
  actions_row.alignment = ft.MainAxisAlignment.CENTER

  page.add(alarm_audio, title, text_to_show, actions_row)


if __name__ == "__main__":
  ft.app(target=main, view=ft.FLET_APP_WEB, port=8080)
