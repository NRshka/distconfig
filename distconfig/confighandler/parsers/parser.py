class AbstractConfigParser:
    @staticmethod
    def parse(path: str) -> dict:
        raise NotImplementedError()
