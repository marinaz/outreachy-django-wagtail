from __future__ import absolute_import, unicode_literals

from os import urandom
from base64 import urlsafe_b64encode
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.db import models
from django.urls import reverse

from ckeditor.fields import RichTextField as CKEditorField

from modelcluster.fields import ParentalKey

from languages.fields import LanguageField

from timezone_field.fields import TimeZoneField

from wagtail.wagtailcore.models import Orderable
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailadmin.edit_handlers import InlinePanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailadmin.edit_handlers import StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.wagtailembeds.blocks import EmbedBlock

class HomePage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(template="home/blocks/heading.html")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('logo', ImageChooserBlock(template="home/blocks/logo.html")),
        ('date', blocks.DateBlock()),
        ('table', TableBlock(template="home/blocks/table.html")),
        ('quote', blocks.RichTextBlock(template="home/blocks/quote.html")),
    ])
    content_panels = Page.content_panels + [
        StreamFieldPanel('body', classname="full"),
    ]

class RichTextOnly(Page):
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

class RoundsIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

class DonatePage(Page):
    intro = RichTextField(blank=True, default='<p>Individual donations can be made via PayPal, check, or wire. Donations are tax deductible, and are handled by our 501(c)(3) non-profit parent organization, Software Freedom Conservancy. Individual donations are directed to the Outreachy general fund, unless otherwise specified.</p>')
    paypal_text = RichTextField(blank=True, default='<p><strong>PayPal</strong> To donate through PayPal, please click on the "Donate" button below.</p>')
    check_text = RichTextField(blank=True, default='<p><strong>Check</strong> We can accept check donations drawn in USD from banks in the USA. Please make the check payable to "Software Freedom Conservancy, Inc." and put "Directed donation: Outreachy" in the memo field. Please mail the check to: <br/><span class="offset1">Software Freedom Conservancy, Inc.</span><br/><span class="offset1">137 Montague ST Ste 380</span><br/><span class="offset1">Brooklyn, NY 11201</span><br/><span class="offset1">USA</span></p>')
    wire_text = RichTextField(blank=True, default='<p><strong>Wire</strong> Please write to <a href="mailto:accounting@sfconservancy.org">accounting@sfconservancy.org</a> and include the country of origin of your wire transfer and the native currency of your donation to receive instructions for a donation via wire.</p>')
    outro = RichTextField(blank=True, default='<p>If you are a corporation seeking to sponsor Outreachy, please see <a href="https://www.outreachy.org/sponsor/">our sponsor page.</a></p>')

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('paypal_text', classname="full"),
        FieldPanel('check_text', classname="full"),
        FieldPanel('wire_text', classname="full"),
        FieldPanel('outro', classname="full"),
    ]

class StatsRoundFifteen(Page):
    unused = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('unused', classname="full"),
    ]

class RoundPage(Page):
    roundnumber = models.IntegerField()
    pingnew = models.DateField("Date to start pinging new orgs", blank=True, default='2017-08-01')
    pingold = models.DateField("Date to start pinging past orgs", blank=True, default='2017-08-07')
    orgreminder = models.DateField("Date to remind orgs to submit their home pages", blank=True, default='2017-08-14')
    landingdue = models.DateField("Date community landing pages are due", blank=True, default='2017-08-28')
    appsopen = models.DateField("Date applications open", default='2017-09-07')
    lateorgs = models.DateField("Last date to add community landing pages", blank=True, default='2017-10-02')
    appsclose = models.DateField("Date applications are due", blank=True, default='2017-10-23')
    appslate = models.DateField("Date extended applications are due", blank=True, default='2017-10-30')
    internannounce = models.DateField("Date interns are announced", default='2017-11-09')
    internstarts = models.DateField("Date internships start", default='2017-12-05')
    midfeedback = models.DateField("Date mid-point feedback is due", blank=True, default='2018-01-16')
    internends = models.DateField("Date internships end", default='2018-03-05')
    finalfeedback = models.DateField("Date final feedback is due", blank=True, default='2018-03-12')
    sponsordetails = RichTextField(default='<p>Outreachy is hosted by the <a href="https://sfconservancy.org/">Software Freedom Conservancy</a> with special support from Red Hat, GNOME, and <a href="http://otter.technology">Otter Tech</a>. We invite companies and free and open source communities to sponsor internships in the next round.</p>')

    content_panels = Page.content_panels + [
        FieldPanel('roundnumber'),
        FieldPanel('pingnew'),
        FieldPanel('pingold'),
        FieldPanel('orgreminder'),
        FieldPanel('landingdue'),
        FieldPanel('appsopen'),
        FieldPanel('lateorgs'),
        FieldPanel('appsclose'),
        FieldPanel('appslate'),
        FieldPanel('internannounce'),
        FieldPanel('internstarts'),
        FieldPanel('midfeedback'),
        FieldPanel('internends'),
        FieldPanel('finalfeedback'),
        FieldPanel('sponsordetails', classname="full"),
    ]
    def ProjectsDeadline(self):
        return(self.appsclose - timedelta(days=14))

    def LateApplicationsDeadline(self):
        return(self.appsclose + timedelta(days=7))
    
    def InternSelectionDeadline(self):
        return(self.appsclose + timedelta(days=10))
    
    def InternConfirmationDeadline(self):
        return(self.appsclose + timedelta(days=24))

class CohortPage(Page):
    round_start = models.DateField("Round start date")
    round_end = models.DateField("Round end date")
    content_panels = Page.content_panels + [
            FieldPanel('round_start'),
            FieldPanel('round_end'),
            InlinePanel('participant', label="Intern or alumns information", help_text="Please add information about the alumn or intern"),
    ]

class AlumInfo(Orderable):
    page = ParentalKey(CohortPage, related_name='participant')
    name = models.CharField(max_length=255, verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    picture = models.ForeignKey(
            'wagtailimages.Image',
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            related_name='+'
            )
    gravitar = models.BooleanField(max_length=255, verbose_name="Use gravitar image associated with email?")
    location = models.CharField(max_length=255, blank=True, verbose_name="Location (optional)")
    nick = models.CharField(max_length=255, blank=True, verbose_name="Chat/Forum/IRC username (optional)")
    blog = models.URLField(blank=True, verbose_name="Blog URL (optional)")
    rss = models.URLField(blank=True, verbose_name="RSS URL (optional)")
    community = models.CharField(max_length=255, verbose_name="Community name")
    project = models.CharField(max_length=255, verbose_name="Project description")
    mentors = models.CharField(max_length=255, verbose_name="Mentor name(s)")
    panels = [
            FieldPanel('name'),
            FieldPanel('email'),
            ImageChooserPanel('picture'),
            FieldPanel('gravitar'),
            FieldPanel('location'),
            FieldPanel('nick'),
            FieldPanel('blog'),
            FieldPanel('rss'),
            FieldPanel('community'),
            FieldPanel('project'),
            FieldPanel('mentors'),
    ]

# We can't remove this old function because the default value
# for the token field used mentor_id and so an old migration
# refers to mentor_id
# FIXME - squash migrations after applied to server
def mentor_id():
    # should be a multiple of three
    return urlsafe_b64encode(urandom(9))

# There are several project descriptions on the last round page
# that are far too long. This feels about right.
SENTENCE_LENGTH=100
# Current maximum description paragraph on round 15 page is 684.
PARAGRAPH_LENGTH=800
THREE_PARAGRAPH_LENGTH=3000
LONG_LEGAL_NAME=800
SHORT_NAME=100


# From Wordnik:
# comrade: A person who shares one's interests or activities; a friend or companion.
# user: One who uses addictive drugs.
class Comrade(models.Model):
    account = models.OneToOneField(User, primary_key=True)
    public_name = models.CharField(max_length=LONG_LEGAL_NAME, verbose_name="Name (public)", help_text="Your full name, which will be publicly displayed on the Outreachy website. This is typically your given name, followed by your family name. You may use a pseudonym or abbreviate your given or family names if you have concerns about privacy.")

    nick_name = models.CharField(max_length=SHORT_NAME, verbose_name="Nick name (internal)", help_text="The short name used in emails to you. You would use this name when introducing yourself to a new person, such as 'Hi, I'm (nick name)'. Emails will be addressed 'Hi (nick name)'. This name will be shown to organizers, coordinators, mentors, and volunteers.")

    legal_name = models.CharField(max_length=LONG_LEGAL_NAME, verbose_name="Legal name (private)", help_text="Your name on your government identification. This is the name that you would use to sign a legal document. This will be used only by Outreachy organizers on any private legal contracts. Other applicants, coordinators, mentors, and volunteers will not see this name.")

    # Reference: https://uwm.edu/lgbtrc/support/gender-pronouns/
    EY_PRONOUNS = ['ey', 'em', 'eir', 'eirs', 'eirself', 'http://pronoun.is/ey']
    FAE_PRONOUNS = ['fae', 'faer', 'faer', 'faers', 'faerself', 'http://pronoun.is/fae']
    HE_PRONOUNS = ['he', 'him', 'his', 'his', 'himself', 'http://pronoun.is/he']
    PER_PRONOUNS = ['per', 'per', 'pers', 'pers', 'perself', 'http://pronoun.is/per']
    SHE_PRONOUNS = ['she', 'her', 'her', 'hers', 'herself', 'http://pronoun.is/she']
    THEY_PRONOUNS = ['they', 'them', 'their', 'theirs', 'themself', 'http://pronoun.is/they']
    VE_PRONOUNS = ['ve', 'ver', 'vis', 'vis', 'verself', 'http://pronoun.is/ve']
    XE_PRONOUNS = ['xe', 'xem', 'xyr', 'xyrs', 'xemself', 'http://pronoun.is/xe']
    ZE_PRONOUNS = ['ze', 'hir', 'hir', 'hirs', 'hirself', 'http://pronoun.is/ze']
    PRONOUN_CHOICES = (
            (SHE_PRONOUNS[0], '{subject}/{Object}/{possessive}'.format(subject=SHE_PRONOUNS[0], Object=SHE_PRONOUNS[1], possessive=SHE_PRONOUNS[2])),
            (HE_PRONOUNS[0], '{subject}/{Object}/{possessive}'.format(subject=HE_PRONOUNS[0], Object=HE_PRONOUNS[1], possessive=HE_PRONOUNS[1])),
            (THEY_PRONOUNS[0], '{subject}/{Object}/{possessive}'.format(subject=THEY_PRONOUNS[0], Object=THEY_PRONOUNS[1], possessive=THEY_PRONOUNS[2])),
            (FAE_PRONOUNS[0], '{subject}/{Object}/{possessive}'.format(subject=FAE_PRONOUNS[0], Object=FAE_PRONOUNS[1], possessive=FAE_PRONOUNS[2])),
            (EY_PRONOUNS[0], '{subject}/{Object}/{possessive}'.format(subject=EY_PRONOUNS[0], Object=EY_PRONOUNS[1], possessive=EY_PRONOUNS[2])),
            (PER_PRONOUNS[0], '{subject}/{Object}/{possessive}'.format(subject=PER_PRONOUNS[0], Object=PER_PRONOUNS[1], possessive=PER_PRONOUNS[2])),
            (VE_PRONOUNS[0], '{subject}/{Object}/{possessive}'.format(subject=VE_PRONOUNS[0], Object=VE_PRONOUNS[1], possessive=VE_PRONOUNS[2])),
            (XE_PRONOUNS[0], '{subject}/{Object}/{possessive}'.format(subject=XE_PRONOUNS[1], Object=XE_PRONOUNS[2], possessive=XE_PRONOUNS[3])),
            (ZE_PRONOUNS[0], '{subject}/{Object}/{possessive}'.format(subject=ZE_PRONOUNS[1], Object=ZE_PRONOUNS[2], possessive=ZE_PRONOUNS[3])),
            )
    pronouns = models.CharField(
            max_length=4,
            choices=PRONOUN_CHOICES,
            default=THEY_PRONOUNS,
            verbose_name="Pronouns",
            help_text="Your preferred pronoun. This will be used in emails from Outreachy organizers directly to you. The format is subject/object/possessive. Example: '__(subject)__ interned with Outreachy. The mentor liked working with __(object)__. __(possessive)__ project was challenging.",
            )

    pronouns_to_participants = models.BooleanField(
            verbose_name = "Share pronouns with Outreachy participants",
            help_text = "If this box is checked, applicant pronouns will be shared with coordinators, mentors and volunteers. If the box is checked, coordinator and mentor pronouns will be shared with applicants. If you don't want to share your pronouns, all Outreachy organizer email that Cc's another participant will use they/them/their pronouns for you.",
            default=True,
            )

    pronouns_public = models.BooleanField(
            verbose_name = "Share pronouns publicly on the Outreachy website",
            help_text = "Mentor, coordinator, and accepted interns' pronouns will be displayed publicly on the Outreachy website to anyone who is not logged in. Sharing pronouns can be a way for people to proudly display their gender identity and connect with other Outreachy participants, but other people may prefer to keep their pronouns private.",
            default=False,
            )

    timezone = TimeZoneField(blank=True, verbose_name="(Optional) Your timezone", help_text="The timezone in your current location. Shared with other Outreachy participants to help facilitate communication.")

    primary_language = LanguageField(blank=True, verbose_name="(Optional) Primary language", help_text="The spoken/written language you are most comfortable using. Shared with other Outreachy participants to help facilitate communication. Many Outreachy participants have English as a second language, and we want them to find others who speak their native language.")
    second_language = LanguageField(blank=True, verbose_name="(Optional) Second language", help_text="The second language you are most fluent in.")
    third_language = LanguageField(blank=True, verbose_name="(Optional) Third language", help_text="The next language you are most fluent in.")
    fourth_language = LanguageField(blank=True, verbose_name="(Optional) Fourth language", help_text="The next language you are most fluent in.")

    def __str__(self):
        return self.public_name

class Community(models.Model):
    name = models.CharField(
            max_length=50, verbose_name="Community name")
    slug = models.SlugField(
            max_length=50,
            unique=True,
            help_text="Community URL slug: https://www.outreachy.org/communities/SLUG/")

    description = models.CharField(
            max_length=PARAGRAPH_LENGTH,
            help_text="Short description of community. This should be three sentences for someone who has never heard of your community or the technologies involved. Do not put any links in the short description (use the long description instead).")

    long_description = CKEditorField(
            blank=True,
            help_text="(Optional) Longer description of community.")

    website = models.URLField(
            blank=True,
            help_text="(Optional) Please provide the URL for your FOSS community's website")

    rounds = models.ManyToManyField(RoundPage, through='Participation')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('community-read-only', kwargs={'slug': self.slug})

    def is_coordinator(self, user):
        return self.coordinatorapproval_set.filter(approved=True, coordinator__account=user).exists()

class NewCommunity(Community):
    community = models.OneToOneField(Community, primary_key=True, parent_link=True)

    SMOL = '3'
    TINY = '5'
    MEDIUM = '10'
    SIZABLE = '20'
    BIG = '50'
    LARGER = '100'
    GINORMOUS = '999'
    COMMUNITY_SIZE_CHOICES = (
        (SMOL, '1-3 people'),
        (TINY, '3-5 people'),
        (MEDIUM, '5-10 people'),
        (SIZABLE, '11-20 people'),
        (BIG, '21-50 people'),
        (LARGER, '50-100 people'),
        (GINORMOUS, 'More than 100 people'),
    )
    community_size = models.CharField(
        max_length=3,
        choices=COMMUNITY_SIZE_CHOICES,
        default=SMOL,
        help_text="How many people are contributing to this community regularly?",
    )

    THREE_MONTHS = '3M'
    SIX_MONTHS = '6M'
    ONE_YEAR = '1Y'
    TWO_YEARS = '2Y'
    OLD_YEARS = 'OL'
    LONGEVITY_CHOICES = (
        (THREE_MONTHS, '0-3 months'),
        (SIX_MONTHS, '3-6 months'),
        (ONE_YEAR, '6-12 months'),
        (TWO_YEARS, '1-2 years'),
        (OLD_YEARS, 'More than 2 years'),
    )
    longevity = models.CharField(
        max_length=2,
        choices=LONGEVITY_CHOICES,
        default=THREE_MONTHS,
        help_text="How long has the community been a free and open source software (FOSS) community?",
    )

    participating_orgs = models.CharField(max_length=THREE_PARAGRAPH_LENGTH,
            help_text="What different organizations and companies participate in the project?")

    approved_license = models.BooleanField(help_text='I assert that all Outreachy projects under my community will be released under either an <a href="https://opensource.org/licenses/alphabetical">OSI-approved open source license</a> that is also identified by the FSF as a <a href="https://www.gnu.org/licenses/license-list.html">free software license</a>, OR a <a href="https://creativecommons.org/share-your-work/public-domain/freeworks/">Creative Commons license approved for free cultural works</a>')
    unapproved_license_description = models.CharField(max_length=THREE_PARAGRAPH_LENGTH,
            blank=True,
            help_text="(Optional) If your community uses a license that is not an OSI-approved license or a Creative Commons license, please provide links to the licenses or a description.")

    no_proprietary_software = models.BooleanField(help_text='I assert all Outreachy projects under my community will not rely or build upon proprietary software.')
    proprietary_software_description = models.CharField(max_length=THREE_PARAGRAPH_LENGTH,
            blank=True,
            help_text="(Optional) If your community relies or builds upon proprietary software, please provide description of what software is used.")

    goverance = models.URLField(blank=True, help_text="(Optional) Please provide a URL for a description of your community's governance model")
    code_of_conduct = models.URLField(blank=True, help_text="(Optional) Please provide a URL for to your community's Code of Conduct")
    cla = models.URLField(blank=True, help_text="(Optional) Please provide a URL for your community's Contributor License Agreement (CLA)")
    dco = models.URLField(blank=True, help_text="(Optional) Please provide a URL for your community's Developer Certificate of Origin (DCO) agreement")

class Participation(models.Model):
    community = models.ForeignKey(Community)
    participating_round = models.ForeignKey(RoundPage)

    interns_funded = models.IntegerField(
            verbose_name="How many interns do you expect to fund for this round? (Include any Outreachy community credits to round up to an integer number.)")
    cfp_text = models.CharField(max_length=THREE_PARAGRAPH_LENGTH,
            verbose_name="Additional information to provide on a call for mentors and volunteers page (e.g. what kinds of projects you're looking for, ways for volunteers to help Outreachy applicants)")
    reason_for_not_participating = models.CharField(max_length=THREE_PARAGRAPH_LENGTH,
            blank=True,
            verbose_name="Please let Outreachy organizers know why your community won't be participating in this Outreachy round, and if there's anything we can do to help. This private information is only used by the Outreachy organizers, and will not be displayed on your community page.")
    # FIXME: hide this for everyone except those in the organizer group (or perhaps admin for now)
    list_community = models.NullBooleanField(
            default=None,
            verbose_name="Organizers: Check this box once you have reviewed the community information, confirmed funding, and collected billing information")

    def __str__(self):
        return '{start:%Y %B} to {end:%Y %B} round - {community}'.format(
                community = self.community.name,
                start = self.participating_round.internstarts,
                end = self.participating_round.internends,
                )
    def get_absolute_url(self):
        return reverse('community-landing', kwargs={'round_slug': self.participating_round, 'slug': self.community.slug})

class Project(models.Model):
    project_round = models.ForeignKey(Participation, verbose_name="Outreachy round and community")
    mentors = models.ManyToManyField(Comrade, through='MentorApproval')

    THREE_MONTHS = '3M'
    SIX_MONTHS = '6M'
    ONE_YEAR = '1Y'
    TWO_YEARS = '2Y'
    OLD_YEARS = 'OL'
    LONGEVITY_CHOICES = (
        (THREE_MONTHS, '0-3 months'),
        (SIX_MONTHS, '3-6 months'),
        (ONE_YEAR, '6-12 months'),
        (TWO_YEARS, '1-2 years'),
        (OLD_YEARS, 'More than 2 years'),
    )
    longevity = models.CharField(
        max_length=2,
        choices=LONGEVITY_CHOICES,
        default=THREE_MONTHS,
        help_text="How long has the project accepted contributions from external contributors?",
    )

    SMOL = '3'
    TINY = '5'
    MEDIUM = '10'
    SIZABLE = '20'
    BIG = '50'
    LARGER = '100'
    GINORMOUS = '999'
    COMMUNITY_SIZE_CHOICES = (
        (SMOL, '1-3 people'),
        (TINY, '3-5 people'),
        (MEDIUM, '5-10 people'),
        (SIZABLE, '11-20 people'),
        (BIG, '21-50 people'),
        (LARGER, '50-100 people'),
        (GINORMOUS, 'More than 100 people'),
    )
    community_size = models.CharField(
        max_length=3,
        choices=COMMUNITY_SIZE_CHOICES,
        default=SMOL,
        help_text="How many people are contributing to this project regularly?",
    )
    intern_benefits = models.CharField(
            max_length=PARAGRAPH_LENGTH,
            blank=True,
            help_text='What will the intern learn from working on this project?')
    community_benefits = models.CharField(
            blank=True,
            max_length=PARAGRAPH_LENGTH,
            help_text='How will this project benefit the parent FOSS community?')

    approved_license = models.BooleanField(help_text='I assert that my project is released under either an <a href="https://opensource.org/licenses/alphabetical">OSI-approved open source license</a> that is also identified by the FSF as a <a href="https://www.gnu.org/licenses/license-list.html">free software license</a>, OR a <a href="https://creativecommons.org/share-your-work/public-domain/freeworks/">Creative Commons license approved for free cultural works</a>')

    short_title = models.CharField(
            max_length=SENTENCE_LENGTH,
            help_text='Short project title. This should be 100 characters or less, starting with a verb like "Create", "Improve", "Extend", "Survey", "Document", etc. Assume the applicant has never heard of your technology before and keep it simple.')
    slug = models.SlugField(
            max_length=50,
            verbose_name="Community URL slug: https://www.outreachy.org/communities/SLUG/")
    long_description = CKEditorField(
            blank=True,
            help_text='Description of the project, excluding applicant skills.')

    communication_tool = models.CharField(
            blank=True,
            max_length=SENTENCE_LENGTH,
            help_text='(Optional) Name of the communication tool your project uses. E.g. "IRC", "Zulip", or "Discourse"')
    communication_url = models.CharField(blank=True,
            max_length=200,
            validators=[URLValidator(schemes=['http', 'https', 'irc'])],
            help_text='(Optional) URL for your project`s communication channel. For IRC, use irc://<host>[:port]/[channel]. Since many applicants have issues with IRC port blocking at their universities, IRC communication links will use <a href="https://kiwiirc.com/">Kiwi IRC</a> to embed the IRC communications in the project page.')
    communication_norms = CKEditorField(
            blank=True,
            help_text='(Optional) After following the project communication channel link, are there any special instructions? For example: "Join the #outreachy Zulip channel and make sure to introduce yourself.')
    communication_help = models.URLField(blank=True, help_text='(Optional) URL for the user documentation for your communication protocol')

    repository = models.URLField(blank=True, help_text="(Optional) URL for your project's repository or contribution mechanism")
    issue_tracker = models.URLField(blank=True, help_text="(Optional) URL for your project's issue tracker")
    newcomer_issue_tag = models.CharField(
            blank=True,
            max_length=SENTENCE_LENGTH,
            help_text="(Optional) What tag is used for newcomer-friendly issues for your project?")

    contribution_tasks = CKEditorField(
            help_text='Instructions for how applicants can make contributions during the Outreachy application period. Make sure to include links to getting started tutorials or documentation, how applicants can find contribution tasks on your project website or issue tracker, who they should ask for tasks, and everything they need to know to get started.')

    accepting_new_applicants = models.BooleanField(help_text='Is this project currently accepting new applicants? If you have an applicant in mind to accept as an intern (or several promising applicants) who have filled out the eligibility information and an application, you can uncheck this box to close the project to new applicants.', default=True)

    # A NullBooleanField can be not set in the database (Null),
    # or it can be set in the database to either True or False.
    # Django maps a Null value in the database to the Python None value.
    # Using a NullBooleanField instead of a BooleanField allows us to track three project states:
    #  * Null/None - Project is pending approval from coordinator
    #  * True - Project has been approved by coordinator
    #  * False - Project has been rejected by coordinator
    list_project = models.NullBooleanField(
            default=None,
            verbose_name="Coordinators: Check this box once you have reviewed the project information")

    class Meta:
        unique_together = (
                ('slug', 'project_round'),
                )

    def __str__(self):
        return '{start:%Y %B} to {end:%Y %B} round - {community} - {title}'.format(
                start = self.project_round.participating_round.internstarts,
                end = self.project_round.participating_round.internends,
                community = self.project_round.community,
                title = self.short_title,
                )

    def is_mentor(self, user):
        return self.mentorapproval_set.filter(approved=True, mentor__account=user).exists()
    def is_pending_mentor(self, user):
        return self.mentorapproval_set.filter(approved=False, mentor__account=user).exists()

class ProjectSkill(models.Model):
    project = models.ForeignKey(Project, verbose_name="Project")

    skill = models.CharField(max_length=SENTENCE_LENGTH, verbose_name="Skill description", help_text="What is one skill an the applicant needs to have in order to apply to your project, or what skill will they need to be willing to learn?")

    TEACH_YOU = 'WTU'
    CONCEPTS = 'CON'
    EXPERIMENTATION = 'EXP'
    FAMILIAR = 'FAM'
    CHALLENGE = 'CHA'
    EXPERIENCE_CHOICES = (
            (TEACH_YOU, 'Mentors are willing to teach this skill to applicants with no experience at all'),
            (CONCEPTS, 'Applicants should have read about the skill'),
            (EXPERIMENTATION, 'Applicants should have used this skill in class or personal projects'),
            (FAMILIAR, 'Applicants should be able to expand on their skills with the help of mentors'),
            (CHALLENGE, 'Applicants who are experienced in this skill will have the chance to expand it further'),
            )
    experience_level = models.CharField(
            max_length=3,
            choices=EXPERIENCE_CHOICES,
            default=TEACH_YOU,
            verbose_name="Expected skill experience level",
            help_text="Choose this carefully! Many Outreachy applicants choose not to apply to a project unless they meet 100% of the project skill criteria.",
            )

    BONUS = 'BON'
    OPTIONAL = 'OPT'
    STRONG = 'STR'
    REQUIRED_CHOICES = (
            (BONUS, "It would be nice if applicants had this skill, but it will not impact intern selection"),
            (OPTIONAL, "Mentors will prefer applicants who have this skill"),
            (STRONG, "Mentors will only accept applicants who have this skill as an intern"),
            )
    required = models.CharField(
            max_length=3,
            choices=REQUIRED_CHOICES,
            default=BONUS,
            verbose_name="Skill impact on intern selection",
            help_text="Is this skill a hard requirement, a preference, or an optional bonus? Choose this carefully! Many Outreachy applicants choose not to apply to a project unless they meet 100% of the project skill criteria.",
            )

    def __str__(self):
        return '{start:%Y %B} to {end:%Y %B} round - {community} - {title} - {skill}'.format(
                start = self.project.project_round.participating_round.internstarts,
                end = self.project.project_round.participating_round.internends,
                community = self.project.project_round.community,
                title = self.project.short_title,
                skill = self.skill,
                )


# This through table records whether a mentor is approved for this project.
# If a mentor creates a project, we set them as approved. The coordinator then reviews the Project.
# If a co-mentor signs up to join a project, we set them as unapproved.
# We want the coordinator to review any co-mentors to ensure
# we don't have a random person signing up who can now see project applications.
class MentorApproval(models.Model):
    # If a Project or a Comrade gets deleted, delete this through table.
    mentor = models.ForeignKey(Comrade, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    approved = models.BooleanField(default=False)
    # TODO
    # Add information about how to contact the mentor for this project
    # e.g. I'm <username> on IRC
    # This will require a new MentorApprovalUpdate view and permissions
    # FIXME add a validator for this field that requires it to be checked
    instructions_read = models.BooleanField(
            default=False,
            help_text='I have read the <a href="/mentor/#mentor">mentor duties</a> and <a href="/mentor/mentor-faq/">mentor FAQ</a>.')
    understands_intern_time_commitment = models.BooleanField(
            default=False,
            help_text='I understand that Outreachy mentors will spend a minimum of 5 hours a week mentoring their intern during the three month internship period')
    understands_applicant_time_commitment = models.BooleanField(
            default=False,
            help_text='I understand that Outreachy mentors often find they must spend more time helping applicants during the application period than helping their intern during the intership period')
    understands_mentor_contract = models.BooleanField(
            default=False,
            help_text='I understand that Outreachy mentors will need to sign a <a href="/documents/1/Outreachy-Program--Mentorship-Terms-of-Participation-May-2017.pdf">mentor contract</a> after they accept an applicant as an intern')

    THREE_MONTHS = '3M'
    SIX_MONTHS = '6M'
    ONE_YEAR = '1Y'
    TWO_YEARS = '2Y'
    OLD_YEARS = 'OL'
    LONGEVITY_CHOICES = (
        (THREE_MONTHS, '0-3 months'),
        (SIX_MONTHS, '3-6 months'),
        (ONE_YEAR, '6-12 months'),
        (TWO_YEARS, '1-2 years'),
        (OLD_YEARS, 'More than 2 years'),
    )
    longevity = models.CharField(
        max_length=2,
        choices=LONGEVITY_CHOICES,
        default=THREE_MONTHS,
        help_text="How long have you been contributing to this project?",
    )
    communication_channel_username = models.CharField(
        max_length=SENTENCE_LENGTH,
        blank=True,
        help_text="What is your username on the project communication channel? (This information will be shared with applicants.)",
    )
    OUTREACHY = 'OUT'
    GOOGLE_SUMMER_OF_CODE = 'GSOC'
    RAILS_GIRLS = 'RAILS'
    OTHER_MENTOR_PROGRAM = 'UNK'
    NOT_MENTORED = 'NOT'
    MENTOR_CHOICES = (
        (OUTREACHY, 'Yes, I have mentored in a past Outreachy round'),
        (GOOGLE_SUMMER_OF_CODE, 'No, but I have mentored for Google Summer of Code or Google Code In'),
        (RAILS_GIRLS, 'No, but I have mentored for Rails Girls Summer of Code'),
        (OTHER_MENTOR_PROGRAM, 'No, but I have mentored with another mentorship program'),
        (NOT_MENTORED, 'No, I have never mentored before'),
    )
    mentored_before = models.CharField(
        max_length=4,
        choices=MENTOR_CHOICES,
        default=NOT_MENTORED,
        help_text="Have you been a mentor for Outreachy before? (Note that Outreachy welcomes first time mentors, but this information allows the coordinator and other mentors to provide extra help to new mentors.)",
    )

    def get_absolute_url(self):
        return reverse('project-read-only', kwargs={'community_slug': self.project.project_round.community.slug, 'project_slug': self.project.slug})

    def __str__(self):
        return '{mentor} - {start:%Y %B} to {end:%Y %B} round - {community} - {title}'.format(
                mentor = self.mentor.public_name,
                start = self.project.project_round.participating_round.internstarts,
                end = self.project.project_round.participating_round.internends,
                community = self.project.project_round.community,
                title = self.project.short_title,
                )

# This through table records whether a coordinator is approved for this community.
# Both the current coordinators and organizers (staff) can approve new coordinators.
class CoordinatorApproval(models.Model):
    # If a Project or a Comrade gets deleted, delete this through table.
    coordinator = models.ForeignKey(Comrade, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    approved = models.NullBooleanField(default=None)

    def __str__(self):
        return '{coordinator} for {community}'.format(
                coordinator = self.coordinator.public_name,
                community = self.community,
                )
