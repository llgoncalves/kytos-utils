"""Translate cli commands to non-cli code."""
from kytos.utils.config import KytosConfig
from kytos.utils.exceptions import KytosException
from kytos.utils.napps import NAppsManager


class NAppsAPI:
    """An API for the command-line interface.

    Use the config file only for required options. Static methods are called
    by the parser and they instantiate an object of this class to fulfill the
    request.
    """

    @classmethod
    def disable(cls, args):
        """Disable subcommand."""
        obj = cls(args)
        obj.assert_napp()
        mgr = obj.get_napps_manager()
        for napp in obj.napps:
            mgr.disable(*napp)

    @classmethod
    def enable(cls, args):
        """Enable subcommand."""
        obj = cls(args)
        obj.assert_napp()
        mgr = obj.get_napps_manager()
        for napp in obj.napps:
            mgr.enable(*napp)

    def __init__(self, args=None):
        """Require parsed arguments.

        Args:
            args (dict): Parsed arguments from cli.
        """
        self.napps = args['<napp>'] if args and '<napp>' in args else []
        self._config = KytosConfig().config['napps']

    def assert_napp(self):
        """Make sure that user provided at least one NApp in cli."""
        if not self.napps:
            raise KytosException("Missing NApps.")

    def get_napps_manager(self):
        """Instance of NAppsManager with settings from config file."""
        return NAppsManager(install_path=self._config['installed_path'],
                            enabled_path=self._config['enabled_path'])

    @classmethod
    def create(cls, args):
        """Bootstrap a basic NApp structure on the current folder."""
        NAppsManager.create_napp()

    @classmethod
    def uninstall(cls, args):
        """Uninstall and delete NApps.

        For local installations, do not delete code outside install_path and
        enabled_path.
        """
        obj = cls(args)
        obj.assert_napp()
        mgr = obj.get_napps_manager()
        for napp in obj.napps:
            mgr.uninstall(*napp)

    @classmethod
    def list(cls, args):
        """List all installed NApps and inform whether they are installed."""
        obj = cls()
        mgr = obj.get_napps_manager()

        # Adding status
        napps = [napp + ('[ie]',) for napp in mgr.get_enabled()]
        napps += [napp + ('[i-]',) for napp in mgr.get_disabled()]
        napps.sort()

        # After sorting, format NApp name and move status to the first position
        napps = [(n[2], n[0] + '/' + n[1]) for n in napps]

        titles = 'Status', 'NApp'

        # Calculate maximum width of columns to be printed
        widths = [max(len(napp[col]) for napp in napps) for col in range(2)]
        widths = [max(w, len(t)) for w, t in zip(widths, titles)]
        widths = tuple(widths)

        header = '\n{:^%d} {:^%d}' % widths
        sep = '{:=^%d} {:=^%d}' % widths
        row = '{:^%d} {}' % widths[:-1]

        print(header.format(*titles))
        print(sep.format('', ''))
        for napp in napps:
            print(row.format(*napp))

        print('\nStatus: (i)nstalled, (e)nabled\n')
