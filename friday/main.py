"""Main CLI entrypoint for FRIDAY."""

from friday.ai_brain import ai_brain
from friday.config import config
from friday.utils import (
    clear_screen,
    get_user_input,
    print_ai_response,
    print_divider,
    print_error,
    print_header,
    print_info,
    print_success,
    print_warning,
    show_help,
)


class FridayAssistant:
    """Interactive terminal shell for the assistant agent."""

    def __init__(self) -> None:
        self.running = False
        self.ai = ai_brain

    def start(self) -> None:
        clear_screen()
        print_header()

        if config.openai_api_key:
            print_success(f"Agent mode active with model {config.openai_model}")
        else:
            print_warning("OpenAI API not configured. FRIDAY is in limited offline mode.")

        print_info("Type 'help' for commands or 'exit' to quit.")
        print_divider()

        self.running = True
        self.main_loop()

    def main_loop(self) -> None:
        while self.running:
            try:
                user_input = get_user_input()
                if user_input is None:
                    self.shutdown()
                    break
                if not user_input:
                    continue

                if self._handle_special_commands(user_input):
                    continue

                print_divider()
                print_info("Thinking...")
                response = self.ai.process_command(user_input)
                print_ai_response(response.get("parameters", {}).get("response", ""))
                print_divider()
            except KeyboardInterrupt:
                print()
                self.shutdown()
                break
            except Exception as exc:
                print_error(f"Unexpected error: {exc}")
                print_divider()

    def _handle_special_commands(self, user_input: str) -> bool:
        command = user_input.lower().strip()

        if command in {"exit", "quit", "bye", "goodbye"}:
            self.shutdown()
            return True

        if command == "help":
            show_help()
            return True

        if command in {"clear", "cls"}:
            clear_screen()
            print_header()
            return True

        if command == "reset":
            self.ai.reset_memory()
            print_success("Conversation memory cleared.")
            return True

        if command == "tools":
            print_info(", ".join(self.ai.list_tools()))
            return True

        if command == "automations":
            automations = self.ai.list_automations()
            if not automations:
                print_info("No saved automations.")
            for item in automations:
                print_info(f"{item['name']}: {item['description']} ({item['step_count']} steps)")
            return True

        if command == "schedules":
            schedules = self.ai.list_schedules()
            if not schedules:
                print_info("No active schedules.")
            for item in schedules:
                print_info(
                    f"{item['job_id']}: {item['automation_name']} every {item['interval']} {item['unit']}"
                )
            return True

        if command == "voice on":
            print_success(self.ai.set_voice_output(True))
            return True

        if command == "voice off":
            print_success(self.ai.set_voice_output(False))
            return True

        if command == "listen":
            try:
                spoken = self.ai.voice.listen_once()
                print_info(f"Heard: {spoken}")
                print_divider()
                response = self.ai.process_command(spoken)
                print_ai_response(response.get("parameters", {}).get("response", ""))
                print_divider()
            except Exception as exc:
                print_error(str(exc))
            return True

        return False

    def shutdown(self) -> None:
        print_divider()
        print_info("Shutting down FRIDAY...")
        self.ai.scheduler.stop()
        print_success("Goodbye.")
        self.running = False


def main() -> None:
    assistant = FridayAssistant()
    assistant.start()


if __name__ == "__main__":
    main()
