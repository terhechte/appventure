import subprocess
import re

files = """
guides/advanced_practical_enum_examples/advanced_enum_usage/comparing_enums.md
guides/advanced_practical_enum_examples/advanced_enum_usage/custom_data_types.md
guides/advanced_practical_enum_examples/advanced_enum_usage/custom_initializers.md
guides/advanced_practical_enum_examples/advanced_enum_usage/extensions.md
guides/advanced_practical_enum_examples/advanced_enum_usage/generic_enums.md
guides/advanced_practical_enum_examples/advanced_enum_usage/intro.md
guides/advanced_practical_enum_examples/advanced_enum_usage/iterating_over_enum_cases.md
guides/advanced_practical_enum_examples/advanced_enum_usage/objective_c_support.md
guides/advanced_practical_enum_examples/advanced_enum_usage/protocols.md
guides/advanced_practical_enum_examples/advanced_enum_usage/raw_representable.md
guides/advanced_practical_enum_examples/advanced_enum_usage/recursive_or_indirect_types.md
guides/advanced_practical_enum_examples/diving_in/associated_values.md
guides/advanced_practical_enum_examples/diving_in/enum_values.md
guides/advanced_practical_enum_examples/diving_in/intro.md
guides/advanced_practical_enum_examples/diving_in/methods_and_properties.md
guides/advanced_practical_enum_examples/diving_in/nesting_enums.md
guides/advanced_practical_enum_examples/diving_in/recap.md
guides/advanced_practical_enum_examples/enums_standard_library.md
guides/advanced_practical_enum_examples/introduction.md
guides/advanced_practical_enum_examples/limitations.md
guides/advanced_practical_enum_examples/practical_use_cases/api_endpoints.md
guides/advanced_practical_enum_examples/practical_use_cases/error_handling.md
guides/advanced_practical_enum_examples/practical_use_cases/games.md
guides/advanced_practical_enum_examples/practical_use_cases/intro.md
guides/advanced_practical_enum_examples/practical_use_cases/linked_lists.md
guides/advanced_practical_enum_examples/practical_use_cases/observer_pattern.md
guides/advanced_practical_enum_examples/practical_use_cases/result_types.md
guides/advanced_practical_enum_examples/practical_use_cases/settings.md
guides/advanced_practical_enum_examples/practical_use_cases/status_codes.md
guides/advanced_practical_enum_examples/practical_use_cases/stringly_typed_code.md
guides/advanced_practical_enum_examples/practical_use_cases/uikit_identifiers.md
guides/advanced_practical_enum_examples/practical_use_cases/units.md
guides/associated_types/associated_types.md
guides/associated_types/associated_types_trouble.md
guides/associated_types/conclusion.md
guides/associated_types/type_erasure/a_box_type.md
guides/associated_types/type_erasure/an_abstract_class.md
guides/associated_types/type_erasure/intro.md
guides/associated_types/type_erasure/putting_it_all_together.md
guides/associated_types/working_around_associated_type_issues/equatable.md
guides/associated_types/working_around_associated_type_issues/hiding_behind_protocols.md
guides/associated_types/working_around_associated_type_issues/method_only_types.md
guides/associated_types/working_around_associated_type_issues/self.md
guides/map_flatmap_reduce_more/a_simple_problem.md
guides/map_flatmap_reduce_more/intro.md
guides/map_flatmap_reduce_more/map.md
guides/map_flatmap_reduce_more/more_examples/chunk.md
guides/map_flatmap_reduce_more/more_examples/group_by.md
guides/map_flatmap_reduce_more/more_examples/interdig.md
guides/map_flatmap_reduce_more/more_examples/interpose.md
guides/map_flatmap_reduce_more/more_examples/intro.md
guides/map_flatmap_reduce_more/more_examples/unique.md
guides/map_flatmap_reduce_more/performance.md
guides/map_flatmap_reduce_more/problem_redux.md
guides/map_flatmap_reduce_more/reduce.md
guides/map_flatmap_reduce_more/reduce_examples.md
guides/optionals/advanced_optionals.md
guides/optionals/extending_optionals.md
guides/optionals/how_to_handle_optionals.md
guides/optionals/intro.md
guides/optionals/why_optionals_are_useful.md
guides/pattern_matching/advanced_pattern_matching/enumeration_case_pattern.md
guides/pattern_matching/advanced_pattern_matching/expressionpattern.md
guides/pattern_matching/advanced_pattern_matching/identifier_pattern.md
guides/pattern_matching/advanced_pattern_matching/pattern_types.md
guides/pattern_matching/advanced_pattern_matching/tuple_pattern.md
guides/pattern_matching/advanced_pattern_matching/type_casting_pattern.md
guides/pattern_matching/advanced_pattern_matching/value_binding_pattern.md
guides/pattern_matching/advanced_pattern_matching/wildcard_pattern.md
guides/pattern_matching/fallthrough_break_labels.md
guides/pattern_matching/finishing_words.md
guides/pattern_matching/intro.md
guides/pattern_matching/language_support/for_case.md
guides/pattern_matching/language_support/guard_case.md
guides/pattern_matching/language_support/if_case.md
guides/pattern_matching/language_support/intro.md
guides/pattern_matching/real_world_examples/applying_ranges.md
guides/pattern_matching/real_world_examples/directory_traversion.md
guides/pattern_matching/real_world_examples/fibonacci.md
guides/pattern_matching/real_world_examples/intro.md
guides/pattern_matching/real_world_examples/legacy_api.md
guides/pattern_matching/real_world_examples/optionals.md
guides/pattern_matching/real_world_examples/type_matches.md
guides/pattern_matching/real_world_examples/word_frequencies.md
guides/pattern_matching/trading_engine.md
guides/swift_reflection/conclusion.md
guides/swift_reflection/custom_mirrors/classes_or_structs.md
guides/swift_reflection/custom_mirrors/collections.md
guides/swift_reflection/custom_mirrors/intro.md
guides/swift_reflection/example/implementation.md
guides/swift_reflection/example/intro.md
guides/swift_reflection/example/performance.md
guides/swift_reflection/introduction.md
guides/swift_reflection/mirrors/creating_a_mirror.md
guides/swift_reflection/mirrors/how_to_use_a_mirror.md
guides/swift_reflection/mirrors/intro.md
guides/swift_reflection/mirrors/what_is_in_a_mirror.md
guides/tuples/absolute_basics/creating_and_accessing_tuples.md
guides/tuples/absolute_basics/tuple_destructuring.md
guides/tuples/absolute_basics/tuples_as_return_types.md
guides/tuples/absolute_basics/tuples_for_pattern_matching.md
guides/tuples/advanced_tuples/anonymous_structs.md
guides/tuples/advanced_tuples/fixed_size_sequences.md
guides/tuples/advanced_tuples/generics.md
guides/tuples/advanced_tuples/intro.md
guides/tuples/advanced_tuples/iteration.md
guides/tuples/advanced_tuples/private_state.md
guides/tuples/advanced_tuples/type_aliases.md
guides/tuples/advanced_tuples/variable_arguments.md
guides/tuples/introduction.md
pages/language_features.md
posts/2014-06-08-writing-simple-syntax-extensions-in-swift.md
posts/2015-06-17-swift-method-overloading-by-protocol.md
posts/2015-06-19-swift-try-catch-asynchronous-closures.md
posts/2015-08-25-optional-throw-swift.md
posts/2015-09-30-getting-iphone6s-foundry-from-swift.md
posts/2015-12-08-swift-ubuntu-x11-window-app.md
posts/2016-03-29-three-tips-for-clean-swift-code.md
posts/2016-04-14-force-optionals-in-guard-or-let-optional-binding.md
posts/2016-04-23-associated-types-enum-raw-value-initializers.md
posts/2016-07-15-swift3-nsdata-data.md
posts/2017-09-30-value-types-for-simple-difference-detection.md
posts/2017-10-08-taming-sourcekitd.md
posts/2018-05-03-expanding-swifts-reach.md
posts/2019-02-24-anonymous-tuple-structs.md
posts/2019-03-17-protocol-composition-untangle-codebase.md
""".split("\n")

def parse_markdown(filename):
    blocks = []
    buffer = []
    begin = False
    for line in open(filename, "r").readlines():
        l = line.strip()
        if len(l) > 3 and l[0:3] == "```" and l.split(" ")[1].lower() == "swift":
            buffer = []
            begin = True
            continue
        if l == "```":
            begin = False
            blocks.append("\n".join(buffer))
            continue
        if begin == True:
            buffer.append(l)
    return blocks

def parse_block(block):
    in_switch = False
    for line in block.split("\n"):
        if len(line) <= 1: continue
        if line.find("switch") >= 0: in_switch = True
        if line.find("case") >= 0 and line[0] != " " and line[0] != "\t" and in_switch:
            return True
    return False

fileset = set()
for filename in files:
    if len(filename.strip()) == 0: continue
    for block in parse_markdown(filename):
        if parse_block(block):
            fileset.add(filename)
for f in fileset:
    print "nvim", f
