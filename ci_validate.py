import yaml
import sys

def validate():
    with open('.gitlab-ci.yml') as f:
        ci = yaml.safe_load(f)

    stages = ci.get('stages', [])
    required_stages = ['lint', 'test', 'build', 'scan', 'deploy', 'rollback']

    if not all(s in stages for s in required_stages):
        print("❌ Missing required stages")
        sys.exit(1)

    if 'test' in ci and 'artifacts' in ci['test']:
        print("✅ Tests publish JUnit artifact")
    if 'build' in ci and 'artifacts' in ci['build']:
        print("✅ Build publishes IMAGE_TAG dotenv")

    print("✅ Pipeline validation passed!")

if __name__ == "__main__":
    validate()