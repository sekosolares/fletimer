from utils.timer import Timer

import flet as ft

def main(page: ft.Page):
  # Sound Effect by https://pixabay.com/es/users/microsammy-22905943/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=8761">Microsammy</a> from <a href="https://pixabay.com/sound-effects//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=8761
  ALARM_AUDIO_SRC = 'clock-alarm.mp3'

  def update_text_count(e, text: str):
    if text == '0':
      text_to_show.value = 'Times Up!'
      on_finish_timer(e)
    else:
      text_to_show.value = text
    page.update()

  def set_text_count(e, text: str):
    text_to_show.value = text
    page.update()

  def stop_countdown(e):
    actions_button.icon = ft.icons.PLAY_ARROW
    actions_button.bgcolor = ft.colors.GREEN
    actions_button.on_click = start_countdown
    actions_button.text = "Start"
    page.update()

    alarm_audio.pause()

    timer.stop()
    actual_countdown = timer.actual_count
    text_to_show.value = f"{actual_countdown}"
    page.update()

  def on_finish_timer(e):
    alarm_audio.volume = 1
    alarm_audio.autoplay = False
    alarm_audio.play()
    page.update()

  def start_countdown(e):
    actions_button.icon = ft.icons.STOP
    actions_button.bgcolor = ft.colors.RED
    actions_button.on_click = stop_countdown
    actions_button.text = "Stop"
    page.update()

    on_time_change(e)

    timer.on_count = lambda: update_text_count(e, f'{timer.actual_count}')
    timer.start()
    update_text_count(e, f'{timer.actual_count}')
    page.update()

  def on_time_change(e):
    if countdown_field.value != '':
      timer.set_default_countdown(int(countdown_field.value))
      set_text_count(e, countdown_field.value)
    else:
      timer.set_default_countdown(0)
      set_text_count(e, '0')

  page.title = "Fletimer"
  page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
  page.vertical_alignment = ft.MainAxisAlignment.CENTER

  title = ft.Text("Fletimer", size=40, weight=ft.FontWeight.BOLD)

  countdown_field = ft.TextField(label="Seconds", value="0")
  countdown_field.on_change = on_time_change

  text_to_show = ft.Text("0", size=40, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE)

  timer = Timer(int(countdown_field.value), in_console=False)

  actions_button = ft.ElevatedButton(
    text="Start",
    on_click=start_countdown,
    bgcolor=ft.colors.GREEN,
    icon=ft.icons.PLAY_ARROW
  )
  actions_button.color = ft.colors.BLACK

  alarm_audio = ft.Audio(
    src=ALARM_AUDIO_SRC,
    balance=0,
    volume=0,
    autoplay=True
  )

  countdown_container = ft.Container(width=100)
  countdown_container.content = countdown_field

  actions_container = ft.Container(width=200)
  actions_container.content = actions_button

  actions_row = ft.Row([countdown_container, actions_container])
  actions_row.alignment = ft.MainAxisAlignment.CENTER

  page.add(alarm_audio, title, text_to_show, actions_row)


if __name__ == "__main__":
  ft.app(target=main, view=ft.FLET_APP_WEB, port=8080)
