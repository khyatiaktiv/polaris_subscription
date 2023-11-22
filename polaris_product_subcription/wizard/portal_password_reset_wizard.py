# -*- coding: utf-8 -*-

import logging

from odoo.tools.translate import _

from odoo import api, fields, models, Command


_logger = logging.getLogger(__name__)


class PortalPasswordResetWizard(models.TransientModel):
    """
    A wizard to manage the reset password of portal users.
    """

    _name = "portal.password.reset.wizard"
    _description = "Reset Portal User Password"

    def _default_partner_ids(self):
        partner_ids = self.env.context.get(
            "default_partner_ids", []
        ) or self.env.context.get("active_ids", [])
        contact_ids = set()
        for partner in self.env["res.partner"].sudo().browse(partner_ids):
            contact_partners = (
                partner.child_ids.filtered(
                    lambda p: p.type in ("contact", "other")
                )
                | partner
            )
            contact_ids |= set(contact_partners.ids)

        return [Command.link(contact_id) for contact_id in contact_ids]

    partner_ids = fields.Many2many(
        "res.partner", string="Partners", default=_default_partner_ids
    )
    user_ids = fields.One2many(
        "portal.password.reset.wizard.user",
        "wizard_id",
        string="Users",
        compute="_compute_user_ids",
        store=True,
        readonly=False,
    )

    @api.depends("partner_ids")
    def _compute_user_ids(self):
        for portal_wizard in self:
            portal_wizard.user_ids = [
                Command.create(
                    {
                        "partner_id": partner.id,
                        "email": partner.email,
                    }
                )
                for partner in portal_wizard.partner_ids
            ]

    @api.model
    def action_open_wizard(self):
        """Create a "portal.password.reset.wizard" and open the form view.

        We need a server action for that because the one2many "user_ids"
        records need to exist to be able to execute a button action on it.
        If they have no ID, the buttons will be disabled, and we won't be
        able to click on them.

        That's why we need a server action, to create the records and then
        open the form view on them.
        """
        portal_reset_password_wizard = self.create({})
        return portal_reset_password_wizard._action_open_modal()

    def _action_open_modal(self):
        """Allow to keep the wizard modal open after executing the action."""
        return {
            "name": _("Portal Reset Password Management"),
            "type": "ir.actions.act_window",
            "res_model": "portal.password.reset.wizard",
            "view_type": "form",
            "view_mode": "form",
            "res_id": self.id,
            "target": "new",
        }


class PortalPasswordResetWizardUser(models.TransientModel):
    """
    A model to configure users in the portal wizard.
    """

    _name = "portal.password.reset.wizard.user"
    _description = "Portal User Config For Password Reset"

    wizard_id = fields.Many2one(
        "portal.password.reset.wizard",
        string="Wizard",
        required=True,
        ondelete="cascade",
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Contact",
        required=True,
        readonly=True,
        ondelete="cascade",
    )
    email = fields.Char("Email")
    user_id = fields.Many2one(
        "res.users",
        string="User",
        compute="_compute_user_id",
        compute_sudo=True,
    )
    password_reset = fields.Char("Password")
    confirm_password_reset = fields.Char("Confirm Password")
    password_match = fields.Boolean(
        "Passwords Match", compute="_compute_password_match"
    )

    @api.depends("password_reset", "confirm_password_reset")
    def _compute_password_match(self):
        for record in self:
            record.password_match = False
            if (
                record.password_reset
                and record.confirm_password_reset
                and record.password_reset != record.confirm_password_reset
            ):
                record.password_match = True

    @api.depends("partner_id")
    def _compute_user_id(self):
        for portal_wizard_user in self:
            user = portal_wizard_user.partner_id.with_context(
                active_test=False
            ).user_ids
            portal_wizard_user.user_id = user[0] if user else False

    def action_reset_password(self):
        """Reset the password of the user.
        If the partner has a linked user, we will reset the user password.
        """
        self.ensure_one()
        if self.password_reset and self.confirm_password_reset:
            self.user_id.sudo().write({"password": self.password_reset})
        return self.wizard_id._action_open_modal()
