from django.test import TestCase

from purbeurre.accounts.models import CustomUser, CustomUserManager

class CustomUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = CustomUser.objects.create(
            email='test@gmail.com', 
            name='Bob'
            )
        # import pdb; pdb.set_trace()
        

    def test_object_name_is_just_name(self):
        expected_object_name = 'Bob'
        self.assertEquals(
            expected_object_name,
            self.user.get_short_name()
        )

    def test_email_is_cleaned(self):
        self.user.clean()
        self.assertEquals(
            self.user.email,
            'test@gmail.com'
            )

class CustomUserManagerModelTest(TestCase):
    # @classmethod
    # def setUpTestData(cls):
    #     # Set up non-modified objects used by all test methods
    #     CustomUser.objects.create(email='test@gmail.com', name='Bob')

    def test_an_user_can_be_created(self):
        user = CustomUser.objects.create_user(
            email='test2@gmail.com', 
            name='Bob2',
            password='testpassword'
            )
        self.assertIsInstance(user, CustomUser)
    
    def test_a_superuser_can_be_created(self):
        new_user = CustomUser.objects.create_superuser(
            email='test2@gmail.com', 
            name='Bob2',
            password='testpassword'
            )
        self.assertIsInstance(new_user, CustomUser)
    
    def user_cant_be_created_without_email(self):
        CustomUser.objects._create_user( 
            name='Bob2',
            password='testpassword'
            )
        self.assertRaises(ValueError)