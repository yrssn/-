package com.yrssn.service.Impl;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.yrssn.mapper.UserMapper;
import com.yrssn.pojo.User;
import com.yrssn.service.UserService;
import org.springframework.stereotype.Service;

@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {
}
