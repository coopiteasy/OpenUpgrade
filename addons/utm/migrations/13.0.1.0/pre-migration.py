# Copyright 2020 ForgeFlow <http://www.forgeflow.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade

_model_renames = [
    ('mail.mass_mailing.stage', 'utm.stage'),
    ('mail.mass_mailing.tag', 'utm.tag'),
]

_table_renames = [
    ('mail_mass_mailing_stage', 'utm_stage'),
    ('mail_mass_mailing_tag', 'utm_tag'),
    ('mail_mass_mailing_tag_rel', 'utm_tag_rel'),
]

_xmlid_renames = [
    ('mass_mailing.campaign_stage_1',
     'utm.campaign_stage_1'),
    ('mass_mailing.campaign_stage_2',
     'utm.campaign_stage_2'),
    ('mass_mailing.campaign_stage_3',
     'utm.campaign_stage_3'),
]


def move_mailing_campaign_to_utm_campaign(env):
    openupgrade.add_fields(env, [
        ("user_id", "utm.campaign", "utm_campaign", "integer", False, "utm"),
        ("stage_id", "utm.campaign", "utm_campaign", "integer", False, "utm"),
        ("color", "utm.campaign", "utm_campaign", "integer", False, "utm"),
    ])
    openupgrade.logged_query(
        env.cr, """
        UPDATE utm_campaign uc
        SET user_id = mmc.user_id, stage_id = mmc.stage_id, color = mmc.color
        FROM mail_mass_mailing_campaign mmc
        WHERE mmc.campaign_id = uc.id"""
    )
    openupgrade.logged_query(
        env.cr, """
        UPDATE utm_tag_rel utr
        SET campaign_id = mmc.campaign_id
        FROM mail_mass_mailing_campaign mmc
        WHERE mmc.id = utr.campaign_id"""
    )


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr
    if openupgrade.table_exists(cr, 'mail_mass_mailing_stage'):
        openupgrade.rename_models(cr, _model_renames)
        openupgrade.rename_tables(cr, _table_renames)
        move_mailing_campaign_to_utm_campaign(env)
        openupgrade.rename_xmlids(cr, _xmlid_renames)
        openupgrade.set_xml_ids_noupdate_value(
            env,
            "utm",
            [
                "campaign_stage_1",
                "campaign_stage_2",
                "campaign_stage_3",
            ],
            False,
        )
