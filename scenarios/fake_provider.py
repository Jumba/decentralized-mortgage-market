import random

from faker import Factory
from faker.providers import BaseProvider

from market import Global


class IBANProvider(BaseProvider):
    dataset = [
        'NL27KABA0162043651',
        'NL67MHCB0631478299',
        'NL04KRED0306142090',
        'NL59ISBK0735281297',
        'NL11CITC0239127846',
        'NL65INSI0849606454',
        'NL88VOWA0281401004',
        'NL70OVBN0710236476',
        'NL16LOYD0841468257',
        'NL56HAND0016151852',
        'NL35BOFS0204076609',
        'NL52STAL0609235168',
        'NL19BKCH0093683650',
        'NL10BMEU0102397546',
        'NL11KNAB0748401849',
        'NL61ISBK0607485604',
        'NL69HSBC0783819692',
        'NL12BOFS0673798844',
        'NL21KABA0523300956',
        'NL81KABA0074860534',
        'NL83KNAB0971795045',
        'NL06ANAA0251942155',
        'NL61FLOR0740670824',
        'NL68NWAB0923095802',
        'NL75ASRB0591613476',
        'NL55ASRB0381005496',
        'NL33STAL0606280405',
        'NL45BOFA0728127571',
        'NL77INGB0830507299',
        'NL78LOCY0276797329',
        'NL41FBHL0546451683',
        'NL15FVLB0867338245',
        'NL82INGB0513309934',
        'NL12BICK0545588596',
        'NL60KRED0673684946',
        'NL82HHBA0896642100',
        'NL60NWAB0452219825',
        'NL64BICK0646880977',
        'NL12KASA0634056905',
        'NL29CITI0179606670',
        'NL96UGBI0467148856',
        'NL89BNPA0733279651',
        'NL17ICBK0236164260',
        'NL15BOFS0807264776',
        'NL48ANAA0713980141',
        'NL16BOFA0652488269',
        'NL94FBHL0995656274',
        'NL12STAL0667053999',
        'NL78BKCH0308327292',
        'NL85ARBN0620474262',
        'NL03ARBN0902810340',
        'NL35ZWLB0084368306',
        'NL55FVLB0972271252',
        'NL82NWAB0658959506',
        'NL83DEUT0028623886',
        'NL03BMEU0466524226',
        'NL78FTSB0139068627',
        'NL47FTSB0665363249',
        'NL52ASNB0209851287',
        'NL32ANAA0588946265',
        'NL59ARTE0147571820',
        'NL27BCIT0736105700',
        'NL60BKMG0325791724',
        'NL35RBRB0513984070',
        'NL51RBRB0307541495',
        'NL79KABA0946817820',
        'NL78ARSN0612096327',
        'NL90HSBC0297939912',
        'NL92BCIT0227810465',
        'NL30BOFS0639056903',
        'NL61NWAB0248982982',
        'NL94ATBA0899474179',
        'NL67DNIB0020790392',
        'NL88LOYD0780111842',
        'NL63FLOR0017395429',
        'NL48COBA0521095220',
        'NL71BNGH0791566315',
        'NL08INSI0416203914',
        'NL91DHBN0183200535',
        'NL31TEBU0077607694',
        'NL41BICK0216614805',
        'NL64STAL0492836698',
        'NL44HHBA0852965915',
        'NL27BKCH0265462940',
        'NL14BMEU0376438673',
        'NL78KRED0394301730',
        'NL32UGBI0437724670',
        'NL07CHAS0015233901',
        'NL95SOGE0187806853',
        'NL64KASA0971600643',
        'NL45FBHL0916181758',
        'NL29TEBU0307607631',
        'NL09ICBK0921626738',
        'NL93BCDM0908572948',
        'NL61INSI0932150519',
        'NL69DHBN0279837569',
        'NL97OVBN0778673952',
        'NL31DLBK0254104088',
        'NL86ARTE0199073678',
        'NL50INSI0376029153',
        'NL55LOCY0041775570',
        'NL27DLBK0066746914',
        'NL86AEGO0469149396',
        'NL96KRED0109512316',
        'NL23COBA0255289383',
        'NL74ANDL0093576005',
        'NL59BKCH0794836372',
        'NL85ABNA0060529164',
        'NL51KASA0399223762',
        'NL13CITC0923747699',
        'NL29ASNB0465463967',
        'NL47INSI0108682269',
        'NL92CITI0906148340',
        'NL40STAL0821676539',
        'NL37BOTK0183739051',
        'NL51BCIT0963744674',
        'NL76RABO0211974048',
        'NL71DNIB0201018357',
        'NL95ISBK0502800070',
        'NL28ANDL0134223616',
        'NL75KRED0081508212',
        'NL37HSBC0435699490',
        'NL78CITC0976023709',
        'NL25HSBC0160345030',
        'NL62INGB0685912191',
        'NL93ATBA0856577499',
        'NL86GILL0422418862',
        'NL57FRGH0888140665',
        'NL43DNIB0025213830',
        'NL56LPLN0232557128',
        'NL52FLOR0266338658',
        'NL09BNGH0290898633',
        'NL25ATBA0892620722',
        'NL03OVBN0516146017',
        'NL77ANAA0209582529',
        'NL08DHBN0761754067',
        'NL11FVLB0368472167',
        'NL13BOFA0298427362',
        'NL41BOFS0277077052',
        'NL86LOCY0237195674',
        'NL54BMEU0530889404',
        'NL36AEGO0191300004',
        'NL89KOEX0956335977',
        'NL12DLBK0924471042',
        'NL02ANAA0913743739',
        'NL49ABNA0511561091',
        'NL96VOWA0360178537',
        'NL95CITI0007566379',
        'NL56DLBK0939396319',
        'NL22VOWA0845920561',
        'NL15RABO0578506815',
        'NL29CITI0960177019',
        'NL13FVLB0417010834',
        'NL32CITC0896521494',
        'NL66BOFS0787351989',
        'NL69ANDL0102568189',
        'NL52HAND0639088058',
        'NL46HAND0699588715',
        'NL47ARTE0204114306',
        'NL19NWAB0112852580',
        'NL54FVLB0153791284',
        'NL86KRED0125167326',
        'NL42FVLB0488183480',
        'NL34SOGE0824877373',
        'NL34KOEX0206443838',
        'NL06DEUT0834736594',
        'NL49BOFS0541486977',
        'NL05BLGW0815824343',
        'NL41INSI0117866725',
        'NL16SNSB0889993688',
        'NL63OVBN0169593231',
        'NL46BOTK0778546284',
        'NL39CHAS0543448959',
        'NL05HHBA0300997914',
        'NL46FRGH0657783323',
        'NL96COBA0098883038',
        'NL34TRIO0430849273',
        'NL08BCDM0523567510',
        'NL08RABO0827130260',
        'NL67BBRU0159726557',
        'NL81BCIT0258859296',
        'NL17OVBN0502305029',
        'NL03DEUT0351087567',
        'NL90KOEX0184388813',
        'NL38NNBA0183895223',
        'NL48UGBI0854653953',
        'NL15NWAB0085651524',
        'NL63SNSB0146274830',
        'NL02ANDL0115384065',
        'NL08CITI0233961968',
        'NL52BLGW0468763414',
        'NL06BOTK0898650755',
        'NL96BKMG0244261121',
        'NL49HHBA0858839466',
        'NL19ABNA0619585293',
        'NL70KOEX0901128090',
        'NL93BOFA0231615620',
        'NL94AEGO0739178628',
        'NL73INSI0927548526',
        'NL78ARBN0279422679',
    ]

    def iban(self):
        return random.choice(IBANProvider.dataset)


class FakePayload(object):
    fake = Factory.create('nl_NL')
    fake.add_provider(IBANProvider)

    @classmethod
    def profile(self, role):
        payload = {
            'role': role,
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'email': str(self.fake.safe_email()),
            'iban': self.fake.iban(),
            'phonenumber': str(self.fake.phone_number()),
        }

        # Borrower
        if role == 1:
            payload.update({
                'current_postalcode': str(self.fake.postcode()),
                'current_housenumber': str(self.fake.building_number()),
                'current_address': str(self.fake.address()),
                'documents_list': []
            })

        return payload

    @classmethod
    def create_loan_request(self):
        price = random.randrange(100000, 200000, 1000)
        payload = {
            'postal_code': str(self.fake.postcode()),
            'house_number': str(self.fake.building_number()),
            'address': str(self.fake.address()),
            'house_link': str(self.fake.url()),
            'seller_phone_number': str(self.fake.phone_number()),
            'seller_email': str(self.fake.safe_email()),
            'price': price,
            'mortgage_type': random.randrange(1,2,1),
            'banks': Global.BANKS.values(),
            'description': self.fake.text(),
            'amount_wanted': random.randrange(price - 80000, price, 1000)
        }

        return payload


    @classmethod
    def accept_loan_request(self, loan_request):
        price = random.randrange(100000, 200000, 1000)
        payload = {
            'request_id': loan_request.id,
            'amount': random.randrange(1000, price, 1000),
            'mortgage_type': random.randrange(1,2,1),
            'interest_rate': random.uniform(0, 20),
            'default_rate': random.uniform(0, 20),
            'max_invest_rate': random.uniform(0, 10),
            'duration': random.randint(6, 120),
            'risk': 'A',
            'investors': []
        }

        return payload

    @classmethod
    def reject_loan_request(self, loan_request):
        payload = {
            'request_id': loan_request.id
        }

        return payload

    @classmethod
    def accept_mortgage_offer(self, mortgage):
        payload = {
            'mortgage_id': mortgage.id
        }

        return payload

    @classmethod
    def reject_mortgage_offer(self, mortgage):
        payload = {
            'mortgage_id': mortgage.id
        }

        return payload

    @classmethod
    def place_investment_offer(self, mortgage):
        amount_wanted = random.randrange(40000, 200000, 1000)
        payload = {
            'amount': random.randint(1, 200000),
            'duration':random.randint(6, 120),
            'interest_rate': random.uniform(0, 20),
            'mortgage_id': mortgage.id
        }

        return payload

    @classmethod
    def accept_investment_offer(self, investment_offer):
        payload = {
            'investment_id': investment_offer.id
        }

        return payload

    @classmethod
    def reject_investment_offer(self, investment_offer):
        payload = {
            'investment_id': investment_offer.id
        }

        return payload

    @classmethod
    def load_single_loan_request(self, loan_request):
        payload = {
            'loan_request_id': loan_request.id
        }

        return payload

    @classmethod
    def load_bids(self, mortgage):
        payload = {
            'mortgage_id': mortgage.id
        }

        return payload
