# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing import z2

import unittest


class PwExpiryLayer(PloneSandboxLayer):
    """
    Testing layer for collective.pwexpiry
    """

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """
        Set up Zope
        """
        # Load ZCML
        import collective.pwexpiry

        self.loadZCML(package=collective.pwexpiry)
        self.loadZCML(package=collective.pwexpiry, name="overrides.zcml")

        from OFS.Application import install_package

        install_package(
            app, collective.pwexpiry, collective.pwexpiry.initialize
        )

    def setUpPloneSite(self, portal):
        """
        Set up Plone
        """
        # import default profile
        applyProfile(portal, "collective.pwexpiry:default")

        # Create test content
        # 1. Login as user with Manager privilages
        setRoles(portal, TEST_USER_ID, ["Manager"])
        login(portal, TEST_USER_NAME)

    def tearDownZope(self, app):
        """
        Tear down Zope
        """
        pass


class PwExpiryRobotLayer(PwExpiryLayer):
    """
    Testing layer for collective.pwexpiry robot tests
    """

    def setUpPloneSite(self, portal):
        """
        Set up Plone
        """
        # import default profile
        applyProfile(portal, "collective.pwexpiry:default")
        applyProfile(portal, "collective.pwexpiry:robot_testing")

        # Create test content
        # 1. Login as user with Manager privilages
        setRoles(portal, TEST_USER_ID, ["Manager"])
        login(portal, TEST_USER_NAME)


FIXTURE = PwExpiryLayer()
ROBOT_FIXTURE = PwExpiryRobotLayer()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="PwExpiryLayer:Integration"
)
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="PwExpiryLayer:Functional"
)
ROBOT_TESTING = FunctionalTesting(
    bases=(ROBOT_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name="PwExpiryLayer:Robot",
)


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION_TESTING


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL_TESTING
