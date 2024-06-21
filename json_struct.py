# -*- coding:utf-8 -*-
import json
import os
import sys


def chtype(var):
    """
    get type of variable as str

    Parameter
    ------
    var : any type

    Return
    ------
    type_of_var : str

    """
    return str(type(var)).split('\'')[1]


class visualizer(object):
    """ 
    Visualize the structure of the jsonfile

    Attributes
    ----------
    json : str
        Path of the json file.

    tree : str
        Structure of the json file.

    """

    def __init__(self, jsondata):
        # with open(jsonfile, 'r', encoding='utf-8') as f:
        #     meta = json.load(f)
        self.json = json.loads(jsondata)
        self.tree = ''

        """
        Parameter
        ---------
        jsonfile : str
            Path of the json file.
        
        tree : str
            Structure of the json file.

        """

    def _print(self, s):
        """
        Parameter
        ---------
        s : str
        """
        self.tree += '\n'
        self.tree += s
        print(s)

    def get_sample(self, var, with_sample, level):
        """
        Parameters
        ----------
        var : any type
            Variable.

        with_sample : bool
            Flag of sample visualize mode.

        level : int
            Level of the indent.

        Return
        ------
        s : string
            Sample of the variable.

        """

        if with_sample:
            if not chtype(var) in ['dict', 'list']:
                try:
                    s = '\n' + ' ' * level + '  sample: ' + str(var)
                except:
                    # + str(var.encode('utf-8'))
                    s = '\n' + ' ' * level + '  sample: '
                return s
        return ''

    def _visualize(self, var, level, with_sample=False, from_list=False):
        """
        Parameters
        ----------
        var : any type
            Variable.

        level : int
            Level of the indent.

        with_sample : bool
            Flag of sample visualize mode.

        from_list : bool
            Type of the previous variable is list or not.

        """

        if 'keys' in dir(var):
            if from_list:
                s = ' ' * level + '|- hoge ' + '\t:\t' + chtype(var)
                self._print(s)
                level += 1

            for key in var.keys():
                s = ' ' * level + '|-' + key + '\t:\t' + \
                    chtype(var[key]) + \
                    self.get_sample(var[key], with_sample, level)
                self._print(s)
                self._visualize(var[key], level + 1, with_sample=with_sample)
            self._print('')

        elif 'list' == chtype(var):
            self._visualize(var[0], level + 1,
                            from_list=True, with_sample=with_sample)

        elif from_list:
            s = ' ' * level + '|- hoge ' + '\t:\t' + \
                chtype(var) + self.get_sample(var, with_sample, level)
            self._print(s)

    def visualize(self, with_sample=False, var_direct=None):
        """
        Parameters
        ----------
        with_sample : bool
            If it is True, show the sample value of the variable except list or dict with the structure of the json.

        var_direct : None or any variable
            If it is not None, show the structure of the variable instead of the json file.
        """

        self.tree = ''

        if var_direct is None:
            s = 'json'
            self._print(s)
            self._visualize(self.json, 0, with_sample=with_sample)
        else:
            s = 'var\t:\t' + chtype(var_direct)
            self._print(s)
            self._visualize(var_direct, 0, with_sample=with_sample)


def main():
    # get arguments
    args = sys.argv
    # assert len(args) > 1, 'Any json path is not given.'

    json_path = args[1]
    assert os.path.exists(json_path), 'Json file is not found.'
    with_sample = False
    if len(args) > 2:
        if args[2] == '-s':
            with_sample = True

    # visualize json
    vis = visualizer(json_path)
    vis.visualize(with_sample=with_sample)


if __name__ == '__main__':
    main()
