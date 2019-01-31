#!/usr/bin/env python

import configparser
from jira import JIRA
from github import Github
import os
import git 
import sys
import yaml

#read config file
config = configparser.ConfigParser()
config.read('config.ini')


#get url from JIRA
def get_url_from_jira(ticket_id):
    jira_config = config['JIRA']
    auth_jira = JIRA(server=jira_config['server'],basic_auth=(jira_config['user_name'], jira_config['password']))
    issue = auth_jira.issue(ticket_id)
    url = (issue.fields.description.split()[-1:][0]).strip()
    print('Jira: '+ url)
    return url
    

#fork repository
def fork_repo(repo_url):
    g = Github(config['GITHUB']['access_token'])
    user = g.get_user()
    print('github user: '+ str(user.login))
    repo = g.get_repo(repo_url.replace("https://github.com/","")) #to remove github from url
    print('repo: '+ str(repo))
    return (user.create_fork(repo),repo)

#convert github https to ssh
def ssh_url(https_url):
    return https_url.replace("https://github.com/","git@github.com:")


# clone repo
def clone_repo_create_branch(branch_name,repo_obj,upsream_obj=None):
    base_path = config['LOCAL']['code_path']
    g = git.cmd.Git(base_path)
    if not os.path.isdir(base_path+'/'+repo_obj.name): #directory does not exists so clone
        g.clone(ssh_url(repo_obj.clone_url))
    
    g = git.cmd.Git(base_path+'/'+repo_obj.name) #make new dir as git
    g.checkout('HEAD', b=branch_name)     
    print('checked out the branch')
    return base_path+'/'+repo_obj.name


# resolve repoman file
def resolve_repoman(path):
    None


def write_to_repoman_file(file_path):
    required = {'repository': {'status': '<active|inactive>', 'team': '<your team>','jira': '<your jira project key to file tickets in, ex.: HALP, POKE>','live':'<yes|no|never>'}}
    with open(file_path, 'r') as stream:
        try:
            infile = yaml.load(stream)
            if 'repository' in infile:
                r = infile['repository']
                if 'status' in r:
                    required['repository']['status'] = r['status']
                if 'team' in r:
                    required['repository']['team'] = r['team']
                if 'jira' in r:
                    required['repository']['jira'] = r['jira']
                if 'live' in r:
                    required['repository']['live'] = r['live']
            print('read yaml from: '+ file_path)
        except yaml.YAMLError as exc:
            print(exc)
            
    with open(file_path, 'a') as stream:
        try:
            yaml.dump(required,stream,default_flow_style=False)
            print('write to yaml: '+ file_path)
        except yaml.YAMLError as exc:
            print(exc)
    

def run(ticket_id):
    jira_url = get_url_from_jira(ticket_id)
    (origin_repo,upstream_repo) = fork_repo(jira_url)
    path = clone_repo_create_branch(ticket_id,origin_repo,upstream_repo)
    write_to_repoman_file(path+'/repoman.yaml')


def main():
    if len(sys.argv) != 2:
        print('usage')
        print('repoman-solver.py <jira-id>')
        return
    run(sys.argv[1])

if __name__ == "__main__":
    main()








