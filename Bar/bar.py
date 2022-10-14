from Storm import storm

class Bar:
    def __init__(self) -> None:
        self.storm = storm.Storm()

    def bar_foo_bar(self) -> None:
        print("bar_foo_bar called")

    def bar_using_storm(self) -> None:
        print("bar_using_storm called")
        self.storm.storm_foo_bar()