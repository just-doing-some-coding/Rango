from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.staticfiles import finders
from rango.models import Category
from django.contrib.auth.models import User

# Thanks to Enzo Roiz https://github.com/enzoroiz who made these tests during an internship with us


def create_category(name, views=0, likes=0):
    return Category.objects.create(name=name, views=views, likes=likes)


class GeneralTests(TestCase):
    def test_serving_static_files(self):
        # If using static media properly result is not NONE once it finds rango.jpg
        result = finders.find('images/rango.jpg')
        self.assertIsNotNone(result)


class IndexPageTests(TestCase):
        
    def test_index_contains_hello_message(self):
        # Check if there is the message 'Rango Says'
        # Chapter 4
        response = self.client.get(reverse('index'))
        self.assertIn(b'Rango says', response.content)
         
    def test_index_using_template(self):
        # Check the template used to render index page
        # Chapter 4
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'rango/index.html')

    def test_rango_picture_displayed(self):
        # Check if is there an image called 'rango.jpg' on the index page
        # Chapter 4
        response = self.client.get(reverse('index'))
        self.assertIn(b'img src="/static/images/rango.jpg', response.content)
    
    def test_index_has_title(self):
        # Check to make sure that the title tag has been used
        # And that the template contains the HTML from Chapter 4 
        response = self.client.get(reverse('index'))
        self.assertIn(b'<title>', response.content)
        self.assertIn(b'</title>', response.content)

    # my
    def test_side_categories_menu_with_no_questions(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present.")

    # my
    def test_side_categories_menu(self):
        create_category('Cat1', 100, 200)
        create_category('Cat2', 250, 300)
        create_category('Cat3', 300, 100)
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(response.context['categories'],
                                 ['<Category: Cat2>', '<Category: Cat1>', '<Category: Cat3>'])

    # my
    def test_link_to_about_page(self):
        response = self.client.get(reverse('index'))
        self.assertContains(response, '<a href="%s">About</a>' % reverse('about'), html=True)


class AboutPageTests(TestCase):
        
    def test_about_contains_create_message(self):
        # Check if in the about page is there - and contains the specified message
        # Exercise from Chapter 4
        response = self.client.get(reverse('about'))
        self.assertIn(b'This tutorial has been put together by', response.content)

    def test_about_contain_image(self):
        # Check if is there an image on the about page
        # Chapter 4
        response = self.client.get(reverse('about'))
        self.assertIn(b'img src="/static/images/', response.content)
        
    def test_about_using_template(self):
        # Check the template used to render index page
        # Exercise from Chapter 4 
        response = self.client.get(reverse('about'))

        self.assertTemplateUsed(response, 'rango/about.html')

    # my
    def test_link_to_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertContains(response, '<a href="%s">Index</a>' % reverse('index'), html=True)
        
        
class ModelTests(TestCase):

    def setUp(self):
        try:
            from populate_rango import populate
            populate()
        except ImportError:
            print('The module populate_rango does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')
        except:
            print('Something went wrong in the populate() function :-(')
        
        
    def get_category(self, name):
        
        from rango.models import Category
        try:                  
            cat = Category.objects.get(name=name)
        except Category.DoesNotExist:    
            cat = None
        return cat
        
    def test_python_cat_added(self):
        cat = self.get_category('Python')  
        self.assertIsNotNone(cat)
         
    def test_python_cat_with_views(self):
        cat = self.get_category('Python')
        self.assertEquals(cat.views, 128)
        
    def test_python_cat_with_likes(self):
        cat = self.get_category('Python')
        self.assertEquals(cat.likes, 64)
        

class Chapter4ViewTests(TestCase):
    def test_index_contains_hello_message(self):
        # Check if there is the message 'hello world!'
        response = self.client.get(reverse('index'))
        self.assertIn('Rango says', response.content)

    def test_does_index_contain_img(self):
        # Check if the index page contains an img
        response = self.client.get(reverse('index'))
        self.assertIn('img', response.content)

    def test_about_using_template(self):
        # Check the template used to render index page
        # Exercise from Chapter 4
        response = self.client.get(reverse('about'))

        self.assertTemplateUsed(response, 'rango/about.html')

    def test_does_about_contain_img(self):
        # Check if in the about page contains an image
        response = self.client.get(reverse('about'))
        self.assertIn('img', response.content)

    def test_about_contains_create_message(self):
        # Check if in the about page contains the message from the exercise
        response = self.client.get(reverse('about'))
        self.assertIn('This tutorial has been put together by', response.content)


def create_admin(name='admin', password='admin'):
    # return User.objects.create_superuser(name=name, email=name+'@test.com', password=password, extra_fields={})
    u = User(username=name)
    u.set_password(password)
    u.is_superuser = True
    u.is_staff = True
    u.save()


# my
class PopulateScriptTests(TestCase):
    def test_populated_categories_displayed_in_categories_page_using_admin(self):
        try:
            from populate_rango import populate
            populate()
        except ImportError:
            print('The module populate_rango does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')
        except:
            print('Something went wrong in the populate() function :-(')

        print('Creating admin')
        create_admin()
        print('Admin created, but I don\'t know what I\'m doing. No test here.')


class Chapter5ViewTests(TestCase):

    def setUp(self):
        try:
            from populate_rango import populate
            populate()
        except ImportError:
            print('The module populate_rango does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')
        except:
            print('Something went wrong in the populate() function :-(')

    def get_category(self, name):
        from rango.models import Category
        try:
            cat = Category.objects.get(name=name)
        except Category.DoesNotExist:
            cat = None
        return cat

    def test_python_cat_added(self):
        cat = self.get_category('Python')
        self.assertIsNotNone(cat)

    def test_python_cat_with_views(self):
        cat = self.get_category('Python')

        self.assertEquals(cat.views, 128)

    def test_python_cat_with_likes(self):
        cat = self.get_category('Python')
        self.assertEquals(cat.likes, 64)

    def test_view_has_title(self):
        response = self.client.get(reverse('index'))

        #Check title used correctly
        self.assertIn('<title>', response.content)
        self.assertIn('</title>', response.content)

    # Need to add tests to:
    # check admin interface - is it configured and set up

    def test_admin_interface_page_view(self):
        from admin import PageAdmin
        self.assertIn('category', PageAdmin.list_display)
        self.assertIn('url', PageAdmin.list_display)


class Chapter6ViewTests(TestCase):

    def setUp(self):
        try:
            from populate_rango import populate
            populate()
        except ImportError:
            print('The module populate_rango does not exist')
        except NameError:
            print('The function populate() does not exist or is not correct')
        except:
            print('Something went wrong in the populate() function :-(')


    # are categories displayed on index page?

    # does the category model have a slug field?


    # test the slug field works..
    def test_does_slug_field_work(self):
        from rango.models import Category
        cat = Category(name='how do i create a slug in django')
        cat.save()
        self.assertEqual(cat.slug,'how-do-i-create-a-slug-in-django')

    # test category view does the page exist?


    # test whether you can navigate from index to a category page


    # test does index page contain top five pages?

    # test does index page contain the words "most liked" and "most viewed"

    # test does category page contain a link back to index page?


class Chapter7ViewTests(TestCase):

    def setUp(self):
        try:
            from forms import PageForm
            from forms import CategoryForm

        except ImportError:
            print('The module forms does not exist')
        except NameError:
            print('The class PageForm does not exist or is not correct')
        except:
            print('Something else went wrong :-(')

    pass
    # test is there a PageForm in rango.forms

    # test is there a CategoryForm in rango.forms

    # test is there an add page page?

    # test is there an category page?


    # test if index contains link to add category page
    #<a href="/rango/add_category/">Add a New Category</a><br />


    # test if the add_page.html template exists.

