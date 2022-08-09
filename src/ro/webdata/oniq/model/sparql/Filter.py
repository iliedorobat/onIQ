from ro.webdata.oniq.model.sparql.Pill import Pill


class Filter:
    def __init__(self, pills: [Pill] = None):
        self.pills = pills if pills is not None else []

    def get_filter_pattern(self, indentation='\t'):
        if len(self.pills.targets) == 0 and len(self.pills.conditions) == 0:
            return None

        # TODO: get_conditions_pills_pattern
        statement = self.pills.get_target_pills_pattern()

        return (
            f'{indentation}'
            f'FILTER(\n{statement}\n\t)'
        )
