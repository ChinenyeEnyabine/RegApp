from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from .models import Regulation, Regulator, IndustrySector, RegulationType, Technology

class RegulationModelTests(TestCase):
    def setUp(self):
        self.industry_sector = IndustrySector.objects.create(name="Energy")
        self.regulation_type = RegulationType.objects.create(name="Policy")
        self.technology = Technology.objects.create(name="AI")
        self.regulator = Regulator.objects.create(name="Energy Commission", jurisdiction="Federal")

        self.regulation = Regulation.objects.create(
            title="AI in Energy Policy",
            description="Policy regarding the use of AI in the energy sector.",
            industry_sector=self.industry_sector,
            regulation_type=self.regulation_type,
            technology=self.technology,
            email="contact@energycommission.gov",
            url="https://energycommission.gov/policy/ai",
            regulatorydetails="Detailed regulations about AI in energy."
        )
        self.regulation.regulators.add(self.regulator)

    def test_regulation_creation(self):
        self.assertEqual(self.regulation.title, "AI in Energy Policy")
        self.assertEqual(self.regulation.regulators.count(), 1)
        self.assertEqual(self.regulation.industry_sector.name, "Energy")
        self.assertEqual(self.regulation.regulation_type.name, "Policy")
        self.assertEqual(self.regulation.technology.name, "AI")

    def test_string_representation(self):
        self.assertEqual(str(self.regulation), "AI in Energy Policy")

class RegulationViewsTests(TestCase):
    def setUp(self):
        self.industry_sector = IndustrySector.objects.create(name="Energy")
        self.regulation_type = RegulationType.objects.create(name="Policy")
        self.technology = Technology.objects.create(name="AI")
        self.regulator = Regulator.objects.create(name="Energy Commission", jurisdiction="Federal")
        self.regulation = Regulation.objects.create(
            title="AI in Energy Policy",
            description="Policy regarding the use of AI in the energy sector.",
            industry_sector=self.industry_sector,
            regulation_type=self.regulation_type,
            technology=self.technology,
            email="contact@energycommission.gov",
            url="https://energycommission.gov/policy/ai",
            regulatorydetails="Detailed regulations about AI in energy."
        )
        self.regulation.regulators.add(self.regulator)

    def test_regulation_detail_view(self):
        url = reverse('regulation_detail', args=[self.regulation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'regulations/regulation_detail.html')
        self.assertContains(response, self.regulation.title)
        self.assertContains(response, self.regulation.description)
        self.assertContains(response, self.regulation.email)
        self.assertContains(response, self.regulation.url)

    def test_regulation_list_view(self):
        url = reverse('regulation_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'regulations/regulation_list.html')
        self.assertContains(response, self.regulation.title)

class RegulationTemplateTests(TestCase):
    def setUp(self):
        self.industry_sector = IndustrySector.objects.create(name="Energy")
        self.regulation_type = RegulationType.objects.create(name="Policy")
        self.technology = Technology.objects.create(name="AI")
        self.regulator = Regulator.objects.create(name="Energy Commission", jurisdiction="Federal")
        self.regulation = Regulation.objects.create(
            title="AI in Energy Policy",
            description="Policy regarding the use of AI in the energy sector.",
            industry_sector=self.industry_sector,
            regulation_type=self.regulation_type,
            technology=self.technology,
            email="contact@energycommission.gov",
            url="https://energycommission.gov/policy/ai",
            regulatorydetails="Detailed regulations about AI in energy."
        )
        self.regulation.regulators.add(self.regulator)

    def test_regulation_detail_template_content(self):
        url = reverse('regulation_detail', args=[self.regulation.id])
        response = self.client.get(url)
        self.assertContains(response, '<h1 class="my-4 regulation-title">AI in Energy Policy</h1>', html=True)
        self.assertContains(response, '<strong class="text-primary">Regulators:</strong>', html=True)
        self.assertContains(response, 'Energy Commission', html=True)
        self.assertContains(response, '<a href="mailto:contact@energycommission.gov">contact@energycommission.gov</a>', html=True)
        self.assertContains(response, '<a href="https://energycommission.gov/policy/ai" class="text-link" target="_blank">https://energycommission.gov/policy/ai</a>', html=True)

