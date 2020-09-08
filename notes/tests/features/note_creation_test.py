from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from notes.models import Note, Paragraph
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
        visit(self, reverse("index"))
        self.assertTrue("/accounts/login" in self.selenium.current_url)

        login(self, user)

        visit(self, reverse("index"))
        body = self.selenium.find_element_by_tag_name('body')
        self.assertTrue(has_content(body, "No existen notas"))

        click_on(body, "Nueva nota")

        # Content for the new note
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
        self.assertTrue(reverse('update', args=[note.id]) in self.selenium.current_url)
        self.assertEqual(3, note.paragraphs.count())

        # Editing a note
        body = self.selenium.find_element_by_tag_name('body')
        fill_in(body, "title", "Pisos termicos editados")
        fill_in(body, "paragraphs-0-description", "Distintos tipos de cultivos editados")
        fill_in(body, "paragraphs-0-content", "se clasifican segun la altura sobre el nivel del mar editados")
        fill_in(body, "paragraphs-1-content", "los cultivos se producen segun la temperatura que se precesnta editados")
        fill_in(body, "paragraphs-2-content", "desiertos, llanos, paramos editados")
        fill_in(body, "paragraphs-3-description", "Importancia para el mercado")
        fill_in(body, "paragraphs-3-content", "Segun los cultivos se puede comercializar lo que se produce")
        fill_in(body, "summary", "Los pisos termicos permiten distintos tipos de cultivo segun la tepmeparuta editados")

        click_on(body, "Guardar nota")

        body = self.selenium.find_element_by_tag_name('body')
        note = Note.objects.latest('id')
        self.assertEqual(4, note.paragraphs.count())

        # When returning to the index page the new note should be listed
        visit(self, reverse("index"))
        body = self.selenium.find_element_by_tag_name('body')
        self.assertTrue(has_content(body, "Pisos termicos editados"))
        self.assertFalse(has_content(body, "No existen notas"))

    def test_a_user_opens_an_existing_note_for_printing_or_sharing(self):
        """ An existing note can be open in a tab for printing or sharing via url.
            Viewing does not require login and the url contains a slug instead of the note id.
        """
        note = Note(title="Pisos termicos", summary="Los pisos termicos permiten distintos tipos de cultivo segun la temperatura")
        note.save()

        Paragraph(
            description="Distintos tipos de cultivos",
            content="se clasifican segun la altura sobre el nivel del mar editados",
            note=note
        ).save()

        visit(self, reverse("show", kwargs={'slug': note.slug}))

        body = self.selenium.find_element_by_tag_name('body')
        self.assertTrue(has_content(body, "Pisos termicos"))
        self.assertTrue(has_content(body, "Distintos tipos de cultivos"))
        self.assertTrue(has_content(body, "se clasifican segun la altura sobre el nivel del mar editados"))
        self.assertTrue(has_content(body, "Los pisos termicos permiten distintos tipos de cultivo segun la temperatura"))
