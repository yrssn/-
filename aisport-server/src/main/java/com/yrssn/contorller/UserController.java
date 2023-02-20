package com.yrssn.contorller;


import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.yrssn.pojo.User;
import com.yrssn.service.UserService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.List;

@Slf4j
@Controller
public class UserController {
    @Autowired
    UserService uerServiceImpl;


    @RequestMapping("/login")
    @ResponseBody
    public User test(String username) {
        QueryWrapper<User> queryWrapper=new QueryWrapper();
        queryWrapper.eq("username",username);
        User one = uerServiceImpl.getOne(queryWrapper);
        return one;
    }
    @RequestMapping("/regesit")
    @ResponseBody
    public int test1(User user) {
        QueryWrapper<User> queryWrapper=new QueryWrapper();
        queryWrapper.eq("username",user.getUsername());
        if(uerServiceImpl.getOne(queryWrapper) == null){
            uerServiceImpl.save(user);
            return 1;

        }else {
            return 0;
        }
    }
    @RequestMapping("/delete")
    @ResponseBody
    public int test3(String username){
        QueryWrapper<User> queryWrapper=new QueryWrapper();
        queryWrapper.eq("username",username);
        if (uerServiceImpl.getOne(queryWrapper) == null){
            return 0;
        }else {
            uerServiceImpl.remove(queryWrapper);
            return 1;
        }
    }
    @RequestMapping("/resetpsw")
    @ResponseBody
    public int test4(String username){
        QueryWrapper<User> queryWrapper=new QueryWrapper();
        queryWrapper.eq("username",username);

        if (uerServiceImpl.getOne(queryWrapper) == null){
            return 0;
        }else {
            User user = new User(username,"123456");
            uerServiceImpl.update(user,queryWrapper);
            return 1;
        }
    }
    @RequestMapping("/queryallusers")
    @ResponseBody
    public List<User> test5(){
        return uerServiceImpl.list();

    }

}
