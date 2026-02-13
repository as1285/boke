# -*- coding: utf-8 -*-
"""
测试技术资源模型
"""

from datetime import datetime
from app import db


class TestTechResource(db.Model):
    """测试技术资源网站"""
    __tablename__ = 'test_tech_resources'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # 网站名称
    url = db.Column(db.String(500), nullable=False)   # 网站链接
    description = db.Column(db.Text)                   # 简介
    category = db.Column(db.String(50), nullable=False)  # 分类
    icon = db.Column(db.String(200))                   # 图标URL
    is_recommended = db.Column(db.Boolean, default=False)  # 是否推荐
    sort_order = db.Column(db.Integer, default=0)      # 排序
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'description': self.description,
            'category': self.category,
            'icon': self.icon,
            'is_recommended': self.is_recommended,
            'sort_order': self.sort_order,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


# 默认测试技术资源数据
DEFAULT_TEST_TECH_RESOURCES = [
    # 自动化测试框架
    {
        'name': 'Selenium',
        'url': 'https://www.selenium.dev/',
        'description': '最流行的Web自动化测试框架，支持多种编程语言和浏览器',
        'category': '自动化测试框架',
        'icon': 'https://www.selenium.dev/favicon.ico',
        'is_recommended': True,
        'sort_order': 1
    },
    {
        'name': 'Cypress',
        'url': 'https://www.cypress.io/',
        'description': '现代前端测试框架，实时重载、调试友好、自动等待',
        'category': '自动化测试框架',
        'icon': 'https://www.cypress.io/favicon.ico',
        'is_recommended': True,
        'sort_order': 2
    },
    {
        'name': 'Playwright',
        'url': 'https://playwright.dev/',
        'description': '微软出品的端到端测试框架，支持多浏览器、自动等待、并行执行',
        'category': '自动化测试框架',
        'icon': 'https://playwright.dev/favicon.ico',
        'is_recommended': True,
        'sort_order': 3
    },
    {
        'name': 'Appium',
        'url': 'https://appium.io/',
        'description': '开源移动应用自动化测试框架，支持iOS和Android原生、混合和Web应用',
        'category': '自动化测试框架',
        'icon': 'https://appium.io/favicon.ico',
        'sort_order': 4
    },
    {
        'name': 'Pytest',
        'url': 'https://docs.pytest.org/',
        'description': 'Python最强大的测试框架，简洁、灵活、插件丰富',
        'category': '自动化测试框架',
        'icon': 'https://docs.pytest.org/favicon.ico',
        'is_recommended': True,
        'sort_order': 5
    },
    {
        'name': 'JUnit',
        'url': 'https://junit.org/',
        'description': 'Java单元测试的标准框架，TDD开发必备',
        'category': '自动化测试框架',
        'icon': 'https://junit.org/favicon.ico',
        'sort_order': 6
    },
    {
        'name': 'TestNG',
        'url': 'https://testng.org/',
        'description': 'Java测试框架，支持并发测试、数据驱动、依赖测试',
        'category': '自动化测试框架',
        'icon': 'https://testng.org/favicon.ico',
        'sort_order': 7
    },
    
    # API测试工具
    {
        'name': 'Postman',
        'url': 'https://www.postman.com/',
        'description': '最流行的API开发和测试工具，支持接口调试、自动化测试、Mock服务',
        'category': 'API测试工具',
        'icon': 'https://www.postman.com/favicon.ico',
        'is_recommended': True,
        'sort_order': 1
    },
    {
        'name': 'Swagger',
        'url': 'https://swagger.io/',
        'description': 'API文档和测试工具，支持OpenAPI规范，自动生成文档和测试',
        'category': 'API测试工具',
        'icon': 'https://swagger.io/favicon.ico',
        'is_recommended': True,
        'sort_order': 2
    },
    {
        'name': 'REST Assured',
        'url': 'https://rest-assured.io/',
        'description': 'Java DSL风格的REST API测试框架，简洁优雅',
        'category': 'API测试工具',
        'icon': 'https://rest-assured.io/favicon.ico',
        'sort_order': 3
    },
    {
        'name': 'Requests',
        'url': 'https://requests.readthedocs.io/',
        'description': 'Python HTTP库，简洁优雅的API测试首选',
        'category': 'API测试工具',
        'icon': 'https://requests.readthedocs.io/favicon.ico',
        'sort_order': 4
    },
    {
        'name': 'Hoppscotch',
        'url': 'https://hoppscotch.io/',
        'description': '开源的Postman替代品，轻量级、无需安装、支持WebSocket',
        'category': 'API测试工具',
        'icon': 'https://hoppscotch.io/favicon.ico',
        'sort_order': 5
    },
    
    # 性能测试工具
    {
        'name': 'JMeter',
        'url': 'https://jmeter.apache.org/',
        'description': 'Apache开源性能测试工具，支持HTTP、数据库、JMS等多种协议',
        'category': '性能测试工具',
        'icon': 'https://jmeter.apache.org/favicon.ico',
        'is_recommended': True,
        'sort_order': 1
    },
    {
        'name': 'Gatling',
        'url': 'https://gatling.io/',
        'description': '高性能负载测试工具，Scala编写，支持实时监控和精美报告',
        'category': '性能测试工具',
        'icon': 'https://gatling.io/favicon.ico',
        'is_recommended': True,
        'sort_order': 2
    },
    {
        'name': 'k6',
        'url': 'https://k6.io/',
        'description': '现代化的负载测试工具，使用JavaScript编写测试脚本，开发者友好',
        'category': '性能测试工具',
        'icon': 'https://k6.io/favicon.ico',
        'is_recommended': True,
        'sort_order': 3
    },
    {
        'name': 'Locust',
        'url': 'https://locust.io/',
        'description': 'Python编写的可扩展负载测试工具，支持分布式测试',
        'category': '性能测试工具',
        'icon': 'https://locust.io/favicon.ico',
        'sort_order': 4
    },
    
    # 测试管理工具
    {
        'name': 'TestRail',
        'url': 'https://www.gurock.com/testrail/',
        'description': '专业的测试用例管理平台，支持测试计划、执行、报告',
        'category': '测试管理工具',
        'icon': 'https://www.gurock.com/favicon.ico',
        'is_recommended': True,
        'sort_order': 1
    },
    {
        'name': 'Zephyr',
        'url': 'https://www.getzephyr.com/',
        'description': 'Jira插件，提供完整的测试管理功能',
        'category': '测试管理工具',
        'icon': 'https://www.getzephyr.com/favicon.ico',
        'sort_order': 2
    },
    {
        'name': 'TestLink',
        'url': 'https://www.testlink.org/',
        'description': '开源测试管理系统，支持测试用例、计划、执行和报告',
        'category': '测试管理工具',
        'icon': 'https://www.testlink.org/favicon.ico',
        'sort_order': 3
    },
    
    # 持续集成/持续测试
    {
        'name': 'Jenkins',
        'url': 'https://www.jenkins.io/',
        'description': '最流行的开源CI/CD工具，支持自动化测试流水线',
        'category': '持续集成',
        'icon': 'https://www.jenkins.io/favicon.ico',
        'is_recommended': True,
        'sort_order': 1
    },
    {
        'name': 'GitHub Actions',
        'url': 'https://github.com/features/actions',
        'description': 'GitHub原生CI/CD工具，与代码仓库深度集成',
        'category': '持续集成',
        'icon': 'https://github.com/favicon.ico',
        'is_recommended': True,
        'sort_order': 2
    },
    {
        'name': 'GitLab CI',
        'url': 'https://docs.gitlab.com/ee/ci/',
        'description': 'GitLab内置CI/CD工具，配置简单，支持容器化',
        'category': '持续集成',
        'icon': 'https://gitlab.com/favicon.ico',
        'sort_order': 3
    },
    {
        'name': 'CircleCI',
        'url': 'https://circleci.com/',
        'description': '云原生CI/CD平台，快速、可扩展、支持并行执行',
        'category': '持续集成',
        'icon': 'https://circleci.com/favicon.ico',
        'sort_order': 4
    },
    
    # 代码质量/静态分析
    {
        'name': 'SonarQube',
        'url': 'https://www.sonarqube.org/',
        'description': '开源代码质量管理平台，支持代码审查、漏洞检测、技术债务分析',
        'category': '代码质量',
        'icon': 'https://www.sonarqube.org/favicon.ico',
        'is_recommended': True,
        'sort_order': 1
    },
    {
        'name': 'Codecov',
        'url': 'https://codecov.io/',
        'description': '代码覆盖率分析工具，支持多种语言和CI/CD集成',
        'category': '代码质量',
        'icon': 'https://codecov.io/favicon.ico',
        'sort_order': 2
    },
    {
        'name': 'Coveralls',
        'url': 'https://coveralls.io/',
        'description': '代码覆盖率追踪工具，支持GitHub集成',
        'category': '代码质量',
        'icon': 'https://coveralls.io/favicon.ico',
        'sort_order': 3
    },
    
    # 安全测试
    {
        'name': 'OWASP ZAP',
        'url': 'https://www.zaproxy.org/',
        'description': '开源Web应用安全扫描器，支持自动化安全测试',
        'category': '安全测试',
        'icon': 'https://www.zaproxy.org/favicon.ico',
        'is_recommended': True,
        'sort_order': 1
    },
    {
        'name': 'Burp Suite',
        'url': 'https://portswigger.net/burp',
        'description': '专业Web安全测试工具，渗透测试必备',
        'category': '安全测试',
        'icon': 'https://portswigger.net/favicon.ico',
        'is_recommended': True,
        'sort_order': 2
    },
    {
        'name': 'Snyk',
        'url': 'https://snyk.io/',
        'description': '开发者安全平台，检测依赖漏洞、容器安全、代码安全',
        'category': '安全测试',
        'icon': 'https://snyk.io/favicon.ico',
        'sort_order': 3
    },
    
    # 移动测试
    {
        'name': 'Espresso',
        'url': 'https://developer.android.com/training/testing/espresso',
        'description': 'Google官方Android UI测试框架',
        'category': '移动测试',
        'icon': 'https://developer.android.com/favicon.ico',
        'sort_order': 1
    },
    {
        'name': 'XCUITest',
        'url': 'https://developer.apple.com/documentation/xctest',
        'description': 'Apple官方iOS UI测试框架',
        'category': '移动测试',
        'icon': 'https://developer.apple.com/favicon.ico',
        'sort_order': 2
    },
    {
        'name': 'Detox',
        'url': 'https://wix.github.io/Detox/',
        'description': 'React Native端到端测试框架，灰盒测试',
        'category': '移动测试',
        'icon': 'https://wix.github.io/Detox/favicon.ico',
        'sort_order': 3
    },
    
    # 测试社区/学习资源
    {
        'name': 'Ministry of Testing',
        'url': 'https://www.ministryoftesting.com/',
        'description': '全球最大的软件测试社区，课程、文章、活动丰富',
        'category': '测试社区',
        'icon': 'https://www.ministryoftesting.com/favicon.ico',
        'is_recommended': True,
        'sort_order': 1
    },
    {
        'name': 'Test Automation University',
        'url': 'https://testautomationu.applitools.com/',
        'description': '免费测试自动化学习平台，Applitools出品',
        'category': '测试社区',
        'icon': 'https://testautomationu.applitools.com/favicon.ico',
        'is_recommended': True,
        'sort_order': 2
    },
    {
        'name': 'Software Testing Help',
        'url': 'https://www.softwaretestinghelp.com/',
        'description': '软件测试教程和资源网站，内容全面',
        'category': '测试社区',
        'icon': 'https://www.softwaretestinghelp.com/favicon.ico',
        'sort_order': 3
    },
    {
        'name': 'TesterHome',
        'url': 'https://testerhome.com/',
        'description': '中文测试社区，国内最大的测试技术交流平台',
        'category': '测试社区',
        'icon': 'https://testerhome.com/favicon.ico',
        'is_recommended': True,
        'sort_order': 4
    }
]


def init_test_tech_resources():
    """初始化测试技术资源数据"""
    from app import db
    
    # 检查是否已有数据
    if TestTechResource.query.first():
        return
    
    for resource_data in DEFAULT_TEST_TECH_RESOURCES:
        resource = TestTechResource(**resource_data)
        db.session.add(resource)
    
    db.session.commit()
    print(f"✅ 已初始化 {len(DEFAULT_TEST_TECH_RESOURCES)} 个测试技术资源")
