from Products.CMFCore.utils import getToolByName
import logging

logger = logging.getLogger('uwosh.policy.externalsite.setuphandlers')

def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('uwosh.policy.externalsite_various.txt') is None:
        return

    # Add additional setup code here
    portal = context.getSite()
    if portal:
        if hasattr(portal, 'Members'):
            portal.Members.content_status_modify(workflow_action='retract')
            logger.info('Retracted Members folder OK')
        else:
            logger.info('unable to locate Members folder')

    else:
        logger.info('unable to get portal')

    pg = getToolByName(portal, 'portal_groups', None)
    if pg:
        for id in ['nguyen', 'ledwell', 'petersed', 'herronj', 'cemanj', ]:
            pg.addPrincipalToGroup(id, 'Administrators')
            logger.info('added %s to Administrators group OK' % id)
    else:
        logger.info('unable to get portal_groups')

    defaultFrontPageId = 'uwosh-front-page'
    if hasattr(portal, defaultFrontPageId):
        retval1 = portal[defaultFrontPageId].content_status_modify(workflow_action='publish')
        logger.info('attempt to publish %s returned ''%s''' % (defaultFrontPageId, retval1))
        retval2 = portal.setDefaultPage(defaultFrontPageId)
        logger.info('attempt to set default page to %s returned ''%s''' % (defaultFrontPageId, retval2))
    else:
        logger.info('unable to locate %s' % defaultFrontPageId)

    oldDefaultFrontPageId = 'front-page'
    if hasattr(portal, oldDefaultFrontPageId):
        retval3 = portal[oldDefaultFrontPageId].content_status_modify(workflow_action='retract')
        logger.info('attempt to retract %s returned ''%s''' % (oldDefaultFrontPageId, retval3))
    else:
        logger.info('unable to locate %s' % oldDefaultFrontPageId)

