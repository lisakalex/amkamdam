import yaml
import langid

# Read YAML file
# with open('a.yml', 'r') as file:
#     data = yaml.safe_load(file)

# lang, confidence = langid.classify("体験型宿泊施設の空間JSW Infrastructure has taken delivery of a new, state of the]art dredger from Netherlands based IHC Dredging. This investment into the second dredger, aligns with the companyfs FY2030 growth plan to \u2026 [+440 chars]")
# lang, confidence = langid.classify(" Infrastructure has taken delivery of a new, state of the]art dredger from Netherlands based IHC Dredging. This investment into the second dredger, aligns with the companyfs FY2030 growth plan to \u2026 [+440 chars]")
lang, confidence = langid.classify("Infrastructure has taken delivery of a new")

kak = None
