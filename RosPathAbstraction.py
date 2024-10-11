# ROS2 components : pub/sub, service

# class == Namespace Path
#   variable == Final Endpoint Namespace Path
#   function starts with "_srv_" == Service
#   function starts with "_act_" == Action

# streaming direction => input or output
#    output : Pub a topic
#    output == variable == Pub a topic

#    input  : The instance try to Sub a topic, passive  (try Sub)
#    input == try Sub == {_}variable ({__}variable is private)

import inspect
class RosAbastractBase:

    def _is_private(self,param_name):
        if '__' in param_name or '/__' in param_name:return True
        return False

    def _is_sub(self,param_name):
        if param_name[0]=='_'  or '/_' in param_name:return True
        return False
    
    def _get_pubs(self):
        name = self.__class__.__name__
        params = self._dfs(self)
        params = [(n,v) for f,n,v in self._dfs(self) if not f]
        return [f'{name}/{i}' for i,v in params if not self._is_sub(i)]

    def _get_subs(self):
        name = self.__class__.__name__
        params = [n for f,n,v in self._dfs(self) if not f]
        return [f'{name}/{i}' for i in params if self._is_sub(i)]
    
    def _get_srvs(self):
        name = self.__class__.__name__
        return [f'{name}/{n}' for f,n,v in self._dfs(self) if f]
        
    def _is_function(self, param):
        if inspect.isfunction(param) or type(param).__name__=='method':return True
        return False
    
    def _is_primitive(self, param):
        if param is None:return True
        if self._is_function(param):return True
        return isinstance(param, (str, int, float))
    
    def _dfs(self, param, path='', is_func=False, only_func=False):
        paths = []

        if self._is_primitive(param):
                paths.append((self._is_function(param),path,param))
        else:
            for key, value in inspect.getmembers(param):
                if self._is_private(key):continue
                is_function = self._is_function(value)
                if is_function and key[0]=='_':continue
                new_path = f"{path}/{key}"
                paths.extend(self._dfs(value, new_path, is_function, only_func))
        return paths
    
class TestRosAbastractBase(RosAbastractBase):
    def __init__(self):
        # pubs
        self.name='It is a test.'
        self.time=154541352

        # subs
        self._weather=None

    # services
    def who_I_am(self):
        return f'{self.name} {self.time}'

class RosRoot(RosAbastractBase):
    def __init__(self):
        self.test = TestRosAbastractBase()

    def _get_srvs(self):
        name = self.__class__.__name__
        fs = super()._get_srvs()
        return [f for f in fs if f not in [f'{name}//sub_topic',
                                        f'{name}//call_service',
                                        f'{name}//all_list',
                                        f'{name}//sevice_list',
                                        f'{name}//topic_list']]

    def sub_topic(self,path:str,*args,**kwargs):
        if self._is_sub(path):return 'Cannot sub a "try Sub" topic'
        param = self
        for i in path.split('/'):
            if len(i)==0:continue
            param = getattr(param,i)
            if not self._is_function(param) and self._is_primitive(param):
                return param
        return None

    def call_service(self,path:str,*args,**kwargs):
        param = self
        for i in path.split('/'):
            if len(i)==0:continue
            param = getattr(param,i)
            if self._is_function(param):
                return param(*args,**kwargs)
        return None

    def all_list(self):
        res = '\n----------------------------------------'
        res += '\npub topics:'+'\n'
        res += '\n'.join(self._get_pubs()).replace('RosRoot/','')+'\n'
        res += '\nsub topics:'+'\n'
        res += '\n'.join(self._get_subs()).replace('RosRoot/','')+'\n'
        res += '\nsrv topics:'+'\n'
        res += '\n'.join(self._get_srvs()).replace('RosRoot/','')+'\n'
        res += '----------------------------------------\n'
        return res
    
    def sevice_list(self):
        res = '\n----------------------------------------'
        res += '\nsrv topics:'+'\n'
        res += '\n'.join(self._get_srvs()).replace('RosRoot/','')+'\n'
        res += '----------------------------------------\n'
        return res

    def topic_list(self):
        res = '\n----------------------------------------'
        res += '\npub topics:'+'\n'
        res += '\n'.join(self._get_pubs()).replace('RosRoot/','')+'\n'
        res += '\nsub topics:'+'\n'
        res += '\n'.join(self._get_subs()).replace('RosRoot/','')+'\n'
        res += '----------------------------------------\n'
        return res

root = RosRoot()
print(root.all_list())
print(root.call_service('/test/who_I_am'))
print(root.sub_topic('/test/name'))