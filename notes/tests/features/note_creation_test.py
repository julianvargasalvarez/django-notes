from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from notes.models import Note
from notes.tests.selenium_helpers import visit, fill_in, submit, click_on, submit, has_content, login, select_option
from django.contrib.auth.models import User
from django.urls import reverse

class NoteCreationTest(LiveServerTestCase):
    @classmethod
    def setUpClass(self):
        self.selenium = WebDriver()
        super(NoteCreationTest, self).setUpClass()

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super(NoteCreationTest, self).tearDownClass()

    def test_a_registered_user_creates_a_note_with_title_paragraphs_and_summary(self):
        user = User.objects.create_user('elusuario', 'myemail@mail.com', '12345678')
        user.save()

        # Notes creatin requires user to login
        visit(self, "/notes/")
        print(self.selenium.current_url)
        self.assertTrue("/accounts/login" in self.selenium.current_url)

        login(self, user)

        visit(self, "/notes/")
        body = self.selenium.find_element_by_tag_name('body')
        self.assertTrue(has_content(body, "No existen notas"))

        click_on(body, "Nueva nota")

        body = self.selenium.find_element_by_tag_name('body')
        fill_in(body, "title", "Pisos termicos")
        fill_in(body, "paragraphs-0-description", "Distintos tipos de cultivos")
        fill_in(body, "paragraphs-0-content", "se clasifican segun la altura sobre el nivel del mar")
        fill_in(body, "paragraphs-1-content", "los cultivos se producen segun la temperatura que se precesnta")
        fill_in(body, "paragraphs-2-content", "desiertos, llanos, paramos")
        fill_in(body, "summary", "Los pisos termicos permiten distintos tipos de cultivo segun la tepmeparuta")

        click_on(body, "Guardar nota")

        body = self.selenium.find_element_by_tag_name('body')
        self.assertTrue(has_content(body, "Nota guardada"))
        note = Note.objects.latest('id')
        self.assertTrue(reverse('edit_note', args=[note.id]) in self.selenium.current_url)
        self.assertEqual(3, note.paragraphs.count())

        visit(self, "/notes/")
        body = self.selenium.find_element_by_tag_name('body')
        self.assertTrue(has_content(body, "Pisos termicos"))
        self.assertFalse(has_content(body, "No existen notas"))
